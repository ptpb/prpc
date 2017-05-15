import asyncio

from brpc.transport import MsgpackTransport


class ProtocolClient(asyncio.Protocol):
    def __init__(self, rpc_transport=MsgpackTransport):
        self.rpc_transport = rpc_transport


    def connection_made(self, transport):
        call = self.rpc_transport.serialize_call('__main__.foo', 'abcd', foo='bar')
        transport.write(call)
        print('wrote')


def run_client():
    loop = asyncio.get_event_loop()
    client = loop.create_connection(lambda: ProtocolClient(), 'localhost', 12345)
    loop.run_until_complete(client)
    loop.run_forever()
