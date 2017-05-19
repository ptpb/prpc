from msgpack_ext import msgpack

from prpc.protocol.base import BaseProtocol


class MsgpackProtocol(BaseProtocol):
    message_size = 16 * 1024

    def __init__(self):
        self.unpacker = msgpack.Unpacker()

    def feed(self, data):
        self.unpacker.feed(data)

        gen = (self.decode_message(message_tuple)
               for message_tuple in self.unpacker)

        return gen

    def pack(self, message):
        message_tuple = self.encode_message(message)

        return msgpack.packb(message_tuple)
