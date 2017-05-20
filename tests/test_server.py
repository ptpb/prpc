from asynctest import mock, patch, sentinel

import pytest

from prpc.protocol import base
from prpc.server import Server


@pytest.fixture
@patch.multiple(base.BaseProtocol, __abstractmethods__=set())
def protocol():
    protocol = base.BaseProtocol()

    return protocol


@pytest.fixture
def server(transport, protocol):
    application = mock.Mock()
    application.handle_method.return_value = sentinel.return_value

    server = Server(application, lambda: protocol)

    return server


async def test_handle_message_request(buf, server, transport, protocol):

    transport.messages = [
        base.Request(method=sentinel.method),
    ]

    await server.handle_recv(transport, protocol)

    server.application.handle_method.assert_called_once_with(
        sentinel.method
    )

    assert len(buf) == 1
    assert buf[0].result == sentinel.return_value
    assert buf[0].error is None
    assert buf[0].id == transport.messages[0].id
    assert isinstance(buf[0], base.Response)


async def test_handle_message_notification(buf, server, transport, protocol):

    transport.messages = [
        base.Notification(method=sentinel.method),
    ]

    await server.handle_recv(transport, protocol)

    server.application.handle_method.assert_called_once_with(
        sentinel.method
    )

    assert len(buf) == 0


async def test_handle_message_request_exception(buf, server, transport, protocol):

    transport.messages = [
        base.Request(method=sentinel.method)
    ]

    server.application.handle_method.side_effect = ValueError('fake_error')

    await server.handle_recv(transport, protocol)

    server.application.handle_method.assert_called_once_with(
        sentinel.method
    )

    assert len(buf) == 1
    assert buf[0].result is None
    assert isinstance(buf[0].error, ValueError)
    assert buf[0].error.args == ('fake_error',)
    assert isinstance(buf[0], base.Response)
