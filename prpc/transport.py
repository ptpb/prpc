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
    @staticmethod
    def serialize_call(method_name, *args, **kwargs):
        print('serialize', method_name, args, kwargs)
        uuid = uuid4()

        msg = msgpack.packb([
            uuid,
            method_name,
            args,
            kwargs
        ])

        return msg, uuid

    @staticmethod
    def deserialize_call(data):
        msg = CallMessage(*msgpack.unpackb(data))

        return msg

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
    def deserialize_reply(data):
        msg = ReplyMessage(*msgpack.unpackb(data))

        return msg
