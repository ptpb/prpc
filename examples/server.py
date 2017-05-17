from prpc.service import ServiceBase, rpc
from prpc.server import run_app
from prpc.application import Application


class Service(ServiceBase):
    @rpc
    def foo(self, *args, **kwargs):
        print('foo called', self, args, kwargs)

        return {'my': 'object'}


app = Application([Service])
run_app(app)
