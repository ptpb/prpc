import asyncio

import structlog

from prpc.protocol import base, msgpack


log = structlog.get_logger()

default_protocol = msgpack.MsgpackProtocol


class ProtocolServer(asyncio.Protocol):
    def __init__(self, application, protocol_factory=default_protocol):
        self.application = application
        self.protocol = protocol_factory()

    def connection_made(self, transport):
        self.transport = transport
        peername = transport.get_extra_info('peername')
        log.debug('connection_made', peername=peername)

    def data_received(self, data):
        for message in self.protocol.feed(data):

            # fixme: handle exceptions
            result = self.handle_message(message)
            self.handle_result(message, result)

    def handle_message(self, message):
        assert not isinstance(message, base.Response)

        log.debug('handle_message', message=message)

        result = self.application.handle_method(
            message.method,
            *message.params,
            **message.kparams,
        )

        return result

    def handle_result(self, message, result):
        if isinstance(message, base.Request):
            message = base.Response(
                id=message.id,
                result=result,
            )

            log.debug('handle_result', message=message)

            data = self.protocol.pack(message)

            self.transport.write(data)


def run_app(application, host='::1', port=12345):
    protocol = ProtocolServer(application)

    loop = asyncio.get_event_loop()
    coro = loop.create_server(lambda: protocol, host=host, port=port)
    server = loop.run_until_complete(coro)

    uris = ['{scheme}://{laddr[0]}:{laddr[1]}'.format(scheme='prpc',
                                                      laddr=socket.getsockname())

            for socket in server.sockets]

    log.info('listening_on', uris=uris)

    loop.run_forever()
