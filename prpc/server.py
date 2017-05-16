import asyncio

from prpc.transport import MsgpackTransport


class ProtocolServer(asyncio.Protocol):
    def __init__(self, application, rpc_transport=MsgpackTransport):
        self.application = application
        self.rpc_transport = rpc_transport

    def connection_made(self, transport):
        self.transport = transport
        print('connection')

    def data_received(self, data):
        call = self.rpc_transport.deserialize_call(data)
        cb = self.application.handle_method

        ret = self.rpc_transport.apply_call(call, cb)

        print('apply return', ret)

        reply = self.rpc_transport.serialize_reply(call, ret)

        self.transport.write(reply)


def run_app(application):
    protocol = ProtocolServer(application)

    loop = asyncio.get_event_loop()
    server = loop.create_server(lambda: protocol, port=12345)
    loop.run_until_complete(server)
    print('run_forever')
    loop.run_forever()
