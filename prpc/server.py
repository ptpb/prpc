import structlog
import trio

from prpc.protocol import base, msgpack


log = structlog.get_logger()
default_protocol = msgpack.MsgpackProtocol


class Server:
    def __init__(self, application, protocol_factory=default_protocol):
        self.application = application
        self.protocol_factory = protocol_factory

    async def handle_recv(self, transport, protocol):
        data = await transport.recv(protocol.message_size)

        for message in protocol.feed(data):
            assert not isinstance(message, base.Response)

            # fixme: handle exceptions
            result = await self.handle_message(message)

            if not isinstance(message, base.Request):
                continue

            await self.handle_response(message, result, protocol, transport)

        return data

    async def handle_message(self, message):
        log.debug('handle_message', message=message)

        result = self.application.handle_method(
            message.method,
            *message.params,
            **message.kparams,
        )

        return result

    async def handle_response(self, message, result, protocol, transport):
        response = base.Response(
            id=message.id,
            result=result,
        )

        log.debug('handle_response', response=response)

        data = protocol.pack(response)

        await transport.sendall(data)

    async def __call__(self, transport):
        peername = transport.getpeername()
        log.debug('connection_made', peername=peername)

        protocol = self.protocol_factory()

        while True:
            data = await self.handle_recv(transport, protocol)
            if not data:
                log.debug('connection_closed', peername=peername)
                return


async def _create_server(nursery, server):
    with trio.socket.socket(trio.socket.AF_INET6) as listen:
        listen.bind(('::1', 12345))
        listen.listen()

        while True:
            transport, _ = await listen.accept()
            nursery.spawn(server, transport)


async def create_server(server, *args):
    async with trio.open_nursery() as nursery:
        nursery.spawn(_create_server, nursery, server)


def run_app(application, protocol=default_protocol):
    server = Server(application, protocol)
    trio.run(create_server, server)
