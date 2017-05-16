import pytest

from prpc.transport import base, msgpack


test_data = [
    (
        b'\x95\x01\x01\x02\x03\x04',
        base.Request(id=1, method=2, params=3, kparams=4)
    ),
    (
        b'\x94\x02\x05\x06\x07',
        base.Notification(method=5, params=6, kparams=7)
    ),
    (
        b'\x94\x03\x08\t\n',
        base.Response(id=8, result=9, error=10)
    )
]


@pytest.fixture
def transport():
    return msgpack.MsgpackTransport()


@pytest.mark.parametrize("data,message", test_data)
def test_feed_single(transport, data, message):
    gen = transport.feed(data)
    assert next(gen) == message

    with pytest.raises(StopIteration):
        next(gen)


@pytest.mark.parametrize("data,message", test_data)
def test_pack_single(transport, data, message):

    assert transport.pack(message) == data


def test_feed_multiple(transport):
    data = b''.join(data for data, _ in test_data)

    gen = transport.feed(data)

    for _, message in test_data:
        assert next(gen) == message

    with pytest.raises(StopIteration):
        next(gen)
