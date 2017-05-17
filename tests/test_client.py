import asyncio
from unittest import mock
from unittest.mock import patch, sentinel

import pytest

from prpc.client import ProtocolClient
from prpc.protocol import base


@pytest.fixture
@patch.multiple(base.BaseProtocol, __abstractmethods__=set())
def client(transport):
    protocol = base.BaseProtocol
    client = ProtocolClient(protocol)

    client.connection_made(transport)

    return client


def test_handle_message_response(client):

    message = base.Response(
        id=sentinel.id,
        result=sentinel.result,
    )

    future = mock.Mock()

    client.resolve_response(sentinel.id, lambda: future)

    client.data_received(message)

    future.set_result.assert_called_once_with(
        sentinel.result
    )

    assert client.futures == {}


@pytest.mark.asyncio
async def test_call(buf, client):

    coro = client.call(sentinel.method)

    def resolve_response(*args, **kwargs):
        future = asyncio.Future()
        future.set_result(sentinel.result)
        return future

    with patch.object(ProtocolClient, 'resolve_response', resolve_response):
        result = await coro

    assert result == sentinel.result

    assert len(buf) == 1
    assert buf[0].method == sentinel.method
    assert isinstance(buf[0], base.Request)


def test_cast(buf, client):

    client.cast(sentinel.method)

    assert len(buf) == 1
    assert buf[0].method == sentinel.method
    assert isinstance(buf[0], base.Notification)
