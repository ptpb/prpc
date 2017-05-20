import structlog
import trio

from prpc.protocol import base, msgpack


log = structlog.get_logger()
default_protocol = msgpack.MsgpackProtocol


class Client:
    def __init__(self, transport, protocol_factory=default_protocol):
        self.protocol = protocol_factory()
        self.transport = transport

        self.request_events = {}

    async def handle_recv(self, transport):
        data = await transport.recv(self.protocol.message_size)

        for message in self.protocol.feed(data):
            await self.handle_response(message)

    async def handle_response(self, message):
        log.debug('handle_response', message=message)

        assert isinstance(message, base.Response)

        assert message.id in self.request_events

        event = self.request_events[message.id]

        assert message.result is not None or message.error is not None

        if message.result is not None:
            self.request_events[message.id] = message.result
        if message.error is not None:
            self.request_events[message.id] = message.error

        event.set()

    async def handle_request(self, message):
        log.debug('handle_request', message=message)

        data = self.protocol.pack(message)
        await self.transport.sendall(data)

    async def _resolve_request_init(self, message):
        event = trio.Event()
        self.request_events[message.id] = event

        return event

    async def _resolve_request_fini(self, message, event):
        await event.wait()
        result = self.request_events[message.id]
        del self.request_events[message.id]

        if isinstance(result, BaseException):
            raise result.__class__(*result.args) from result

        return result

    async def resolve_request(self, message):
        assert message.id not in self.request_events

        event = await self._resolve_request_init(message)

        log.debug('resolve_request', sync=event)
        await self.handle_request(message)

        result = await self._resolve_request_fini(message, event)

        return result

    async def __call__(self):
        while True:
            data = await self.handle_recv(self.transport)
            if not data:
                log.debug('connection_closed', peername=self.transport.getpeername())
                return


class LibraryClient:
    def __init__(self, client):
        self.client = client

    async def cast(self, method, *args, **kwargs):
        message = base.Notification(
            method=method,
            params=args,
            kparams=kwargs
        )

        await self.client.handle_request(message)

    async def call(self, method, *args, **kwargs):
        message = base.Request(
            method=method,
            params=args,
            kparams=kwargs
        )

        return await self.client.resolve_request(message)


async def connect(client_cb, host, port, *,
                  library_client_factory=LibraryClient,
                  client_factory=Client):

    with trio.socket.socket(trio.socket.AF_INET6) as transport:
        await transport.connect((host, port))

        log.debug('connection_made', peername=transport.getpeername())

        client = client_factory(transport)
        library_client = library_client_factory(client)

        async with trio.open_nursery() as nursery:
            nursery.spawn(client)
            nursery.spawn(client_cb, library_client)


def run_client(client_cb, host, port, connect_impl=connect):
    trio.run(connect_impl, client_cb, host, port)
