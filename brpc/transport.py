from functools import partial

import msgpack


packb = partial(msgpack.packb, use_bin_type=True)
unpackb = partial(msgpack.unpackb, encoding='utf-8')


class MsgpackTransport:
    @staticmethod
    def serialize_call(method_name, *args, **kwargs):
        print('serialize', method_name, args, kwargs)

        msg = packb([
            method_name,
            args,
            kwargs
        ])

        return msg

    @staticmethod
    def method_call(msg, cb):
        method_name, args, kwargs = unpackb(msg)

        print(method_name, args, kwargs)

        return cb(method_name, *args, **kwargs)
