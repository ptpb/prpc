from brpc.service import ServiceBase
from brpc.decorator import rpc
from brpc.server import run_app
from brpc.application import Application


class Service(ServiceBase):
    @rpc
    def foo(self, *args, **kwargs):
        print('foo called', self, args, kwargs)


app = Application([Service])
run_app(app)
