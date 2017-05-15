from collections import namedtuple


class ServiceMeta(type):
    def __init__(self, name, bases, attrs):
        super().__init__(name, bases, attrs)

        self.rpc_methods = {}

        for k, v in attrs.items():
            if not getattr(v, '_rpc', None):
                continue

            method_name = '.'.join((attrs['__module__'], k))

            self.rpc_methods[method_name] = v


class ServiceBase(metaclass=ServiceMeta):
    pass


ServiceMethodDescriptor = namedtuple('ServiceMethodDescriptor', [
    'method_name',
    'function',
    'service'
])
