from unittest.mock import sentinel
from asynctest import mock, patch

import pytest

from prpc.client import Client, LibraryClient
from prpc.protocol import base


@pytest.fixture
@patch.multiple(base.BaseProtocol, __abstractmethods__=set())
def client(transport):
    protocol = base.BaseProtocol
    client = Client(transport, protocol)

    return client


@pytest.fixture
def library_client(client):
    return LibraryClient(client)


def setattrr(obj, attr, value, ret):
    setattr(obj, attr, value)
    return ret


async def test_handle_response(client):

    message = base.Response(
        id=sentinel.id,
        result=sentinel.result,
    )

    event = await client._resolve_request_init(message)
    await client.handle_response(message)
    result = await client._resolve_request_fini(message, event)

    assert result == sentinel.result
    assert sentinel.id not in client.request_events


async def test_handle_request(buf, client):

    message = base.Request(
        id=sentinel.id
    )

    await client.handle_request(message)

    assert len(buf) == 1
    assert buf[0].id == sentinel.id


@patch.object(Client, 'resolve_request')
async def test_call(mock_resolve_request, library_client):
    args = mock.Mock()
    mock_resolve_request.side_effect = lambda m: setattrr(args, 'message', m, sentinel.result)

    result = await library_client.call(sentinel.method)

    mock_resolve_request.assert_called_once()
    assert isinstance(args.message, base.Request)
    assert args.message.method == sentinel.method
    assert result == sentinel.result


@patch.object(Client, 'handle_request')
async def test_cast(mock_handle_request, library_client):
    args = mock.Mock()
    mock_handle_request.side_effect = lambda m: setattr(args, 'message', m)

    await library_client.cast(sentinel.method)

    mock_handle_request.assert_called_once()
    assert isinstance(args.message, base.Notification)
    assert args.message.method == sentinel.method
