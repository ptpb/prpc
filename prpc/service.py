from collections import namedtuple


def rpc(func_or_name):

    def wrapper(func, name=func_or_name):
        func._rpc = True
        func._rpc_name = name
        return func

    if callable(func_or_name):
        return wrapper(func_or_name, None)

    return wrapper


def namespace(name):

    def wrapper(cls):
        cls._rpc_namespace = name
        return cls

    return wrapper


class ServiceMeta(type):
    _rpc_namespace = None

    def __init__(self, name, bases, attrs):
        super().__init__(name, bases, attrs)

        self.rpc_methods = {}

        for k, v in attrs.items():
            if not getattr(v, '_rpc', None):
                continue

            namespace = self._rpc_namespace or attrs['__module__']
            method_name = v._rpc_name or k

            method_name = '.'.join((namespace, method_name))

            self.rpc_methods[method_name] = v


class ServiceBase(metaclass=ServiceMeta):
    pass


ServiceMethodDescriptor = namedtuple('ServiceMethodDescriptor', [
    'method_name',
    'function',
    'service'
])
