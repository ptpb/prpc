import asyncio

import structlog

from prpc.protocol import base, msgpack


log = structlog.get_logger()

default_protocol = msgpack.MsgpackProtocol


class ProtocolClient(asyncio.Protocol):
    def __init__(self, protocol_factory=default_protocol):
        self.protocol = protocol_factory()

        self.futures = {}

    def connection_made(self, transport):
        self.transport = transport
        peername = transport.get_extra_info('peername')
        log.debug('connection_made', peername=peername)

    def data_received(self, data):
        for message in self.protocol.feed(data):
            self.handle_message(message)

    def handle_message(self, message):
        assert isinstance(message, base.Response)

        log.debug('handle_message', message=message)

        if message.id in self.futures:
            # fixme: handle errors
            self.futures[message.id].set_result(message.result)
            del self.futures[message.id]

    def cast(self, method, *args, **kwargs):
        message = base.Notification(
            method=method,
            params=args,
            kparams=kwargs
        )

        data = self.protocol.pack(message)
        self.transport.write(data)

    async def call(self, method, *args, **kwargs):
        message = base.Request(
            method=method,
            params=args,
            kparams=kwargs
        )

        data = self.protocol.pack(message)

        future = asyncio.Future()
        self.futures[message.id] = future

        self.transport.write(data)

        return await future


class ClientFactory:
    def __init__(self, protocol=ProtocolClient, loop=None):
        self.loop = loop
        if not self.loop:
            self.loop = asyncio.get_event_loop()

        self.protocol = protocol

    def connect(self, host, port):
        client = self.protocol()

        coro = self.loop.create_connection(lambda: client, host, port)
        # fixme: maybe we don't actually want to do this?
        connection = self.loop.run_until_complete(coro)

        #uri = 'prpc://{host}:{port}'.format(host=host, port=port)

        return client
