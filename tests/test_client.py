from unittest.mock import sentinel
from asynctest import patch

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


async def test_call(buf, client, library_client):

    real_handle_request = client.handle_request

    async def handle_request(self, message):
        await real_handle_request(message)
        await client.handle_response(base.Response(
            id=message.id,
            result=sentinel.result,
        ))

    with patch.object(Client, 'handle_request', handle_request):
        result = await library_client.call(sentinel.method)

    assert result == sentinel.result

    assert len(buf) == 1
    assert buf[0].method == sentinel.method
    assert isinstance(buf[0], base.Request)


async def test_cast(buf, library_client):

    await library_client.cast(sentinel.method)

    assert len(buf) == 1
    assert buf[0].method == sentinel.method
    assert isinstance(buf[0], base.Notification)
