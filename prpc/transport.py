from functools import partial
from uuid import uuid4

from msgpack_ext import msgpack


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
    def method_call(msg, cb):
        uuid, method_name, args, kwargs = msgpack.unpackb(msg)

        print(uuid, method_name, args, kwargs)

        return cb(method_name, *args, **kwargs)
