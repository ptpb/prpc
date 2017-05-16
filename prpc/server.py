import asyncio

import structlog

from prpc.transport import MsgpackTransport


log = structlog.get_logger()


class ProtocolServer(asyncio.Protocol):
    def __init__(self, application, rpc_transport=MsgpackTransport):
        self.application = application
        self.rpc_transport = rpc_transport()

    def connection_made(self, transport):
        self.transport = transport
        peername = transport.get_extra_info('peername')
        log.debug('connection_made', peername=peername)

    def data_received(self, data):
        for msg in self.rpc_transport.feed(data):
            self.handle_msg(msg)

    def handle_msg(self, msg):
        call = self.rpc_transport.deserialize_call(msg)

        log.debug('rpc_call', msg_id=str(call.uuid),
                  rpc_method=call.method_name,
                  rpc_args=(call.args, call.kwargs))
                  #rpc_kwargs=call.kwargs)

        cb = self.application.handle_method
        ret = self.rpc_transport.apply_call(call, cb)

        log.debug('rpc_call_return', msg_id=str(call.uuid), return_value=ret)

        reply = self.rpc_transport.serialize_reply(call, ret)

        self.transport.write(reply)


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
