import inspect

import asynctest
import pytest
from trio.testing import trio_test


@pytest.hookimpl(tryfirst=True)
def pytest_pyfunc_call(pyfuncitem):
    if inspect.iscoroutinefunction(pyfuncitem.obj):
        pyfuncitem.obj = trio_test(pyfuncitem.obj)


@pytest.fixture
def buf():
    return []


@pytest.fixture
def transport(buf):
    transport = asynctest.CoroutineMock()

    def write(chunk):
        buf.append(chunk)

    def recv(_):
        return transport.message

    transport.sendall.side_effect = write
    transport.recv.side_effect = recv

    return transport
