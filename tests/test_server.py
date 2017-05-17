from unittest import mock
from unittest.mock import patch, sentinel

import pytest

from prpc.protocol import base
from prpc.server import ProtocolServer


@pytest.fixture
@patch.multiple(base.BaseProtocol, __abstractmethods__=set())
def server(transport):
    application = mock.Mock()
    application.handle_method.return_value = sentinel.return_value

    protocol = base.BaseProtocol
    server = ProtocolServer(application, protocol)

    server.connection_made(transport)

    return server


def test_handle_message_request(buf, server):

    message = base.Request(
        method=sentinel.method,
    )

    server.data_received(message)

    server.application.handle_method.assert_called_once_with(
        sentinel.method
    )

    assert len(buf) == 1
    assert buf[0].result == sentinel.return_value
    assert buf[0].error is None
    assert buf[0].id == message.id
    assert isinstance(buf[0], base.Response)


def test_handle_message_notification(buf, server):

    message = base.Notification(
        method=sentinel.method
    )

    server.data_received(message)

    server.application.handle_method.assert_called_once_with(
        sentinel.method
    )

    assert len(buf) == 0
