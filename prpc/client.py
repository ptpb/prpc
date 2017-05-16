import asyncio

from prpc.transport import MsgpackTransport


class ProtocolClient(asyncio.Protocol):
    def __init__(self, rpc_transport=MsgpackTransport):
        self.rpc_transport = rpc_transport
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def cast(self, method_name, *args, **kwargs):
        msg, _ = self.rpc_transport.serialize_call(method_name, *args, **kwargs)
        self.transport.write(msg)


class ClientFactory:
    def __init__(self, protocol=ProtocolClient, loop=None):
        self.loop = loop
        if not self.loop:
            self.loop = asyncio.get_event_loop()

        self.protocol = protocol

    def connect(self, host, port):
        client = self.protocol()

        connect = self.loop.create_connection(lambda: client, host, port)
        self.loop.run_until_complete(connect)

        return client
