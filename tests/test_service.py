from prpc import service


def test_rpc_callable():
    @service.rpc
    def func():
        pass

    assert getattr(func, '_rpc') is True
    assert getattr(func, '_rpc_name') is None


def test_rpc_name():
    @service.rpc('test_method')
    def func():
        pass

    assert getattr(func, '_rpc') is True
    assert getattr(func, '_rpc_name') == 'test_method'


def test_namespace():
    @service.namespace('test_namespace')
    class cls:
        pass

    assert getattr(cls, '_rpc_namespace') == 'test_namespace'
