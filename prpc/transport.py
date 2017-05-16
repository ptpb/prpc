from collections import namedtuple
from functools import partial
from uuid import uuid4

from msgpack_ext import msgpack


CallMessage = namedtuple('CallMessage', [
    'uuid',
    'method_name',
    'args',
    'kwargs'
])


ReplyMessage = namedtuple('ReplyMessage', [
    'uuid',
    'obj'
])


class MsgpackTransport:
    def __init__(self):
        self.unpacker = msgpack.Unpacker()

    def feed(self, data):
        self.unpacker.feed(data)

        return self.unpacker

    @staticmethod
    def serialize_call(method_name, *args, **kwargs):
        uuid = uuid4()

        msg = msgpack.packb([
            uuid,
            method_name,
            args,
            kwargs
        ])

        return msg, uuid

    @staticmethod
    def deserialize_call(msg):
        call = CallMessage(*msg)

        return call

    @staticmethod
    def apply_call(msg, cb):
        ret = cb(msg.method_name, *msg.args, **msg.kwargs)

        return ret

    @staticmethod
    def serialize_reply(call_msg, obj):
        msg = msgpack.packb([
            call_msg.uuid,
            obj
        ])

        return msg

    @staticmethod
    def deserialize_reply(msg):
        reply = ReplyMessage(*msg)

        return reply
