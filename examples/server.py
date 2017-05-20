from prpc.service import ServiceBase, rpc, namespace
from prpc.server import run_app
from prpc.application import Application


class Service(ServiceBase):
    @rpc
    async def foo(self, *args, **kwargs):
        print('foo called', self, args, kwargs)

        return {'my': 'object'}


app = Application([Service])
run_app(app)
