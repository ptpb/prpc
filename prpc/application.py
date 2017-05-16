import structlog

from prpc.service import ServiceMethodDescriptor


log = structlog.get_logger()


class Application:
    def __init__(self, services):
        self.rpc_methods = {}

        self.register_services(services)

    def register_services(self, services):
        for cls in services:
            service = cls()

            for method_name, function in service.rpc_methods.items():
                descriptor = ServiceMethodDescriptor(
                    method_name=method_name,
                    function=function,
                    service=service
                )

                log.debug("registered_service", rpc_method=method_name, service=service)

                self.rpc_methods[method_name] = descriptor

    def handle_method(self, method_name, *args, **kwargs):
        descriptor = self.rpc_methods[method_name]

        return descriptor.function(descriptor.service, *args, **kwargs)
