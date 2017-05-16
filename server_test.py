from prpc.service import ServiceBase
from prpc.decorator import rpc
from prpc.server import run_app
from prpc.application import Application


class Service(ServiceBase):
    @rpc
    def foo(self, *args, **kwargs):
        print('foo called', self, args, kwargs)


app = Application([Service])
run_app(app)
