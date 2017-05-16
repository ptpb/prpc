import uuid
from unittest.mock import patch

import pytest

from prpc.protocol import base


test_data = [
    (
        (base.MessageType.request, 1, 2, 3, 4),
        base.Request(id=1, method=2, params=3, kparams=4)
    ),
    (
        (base.MessageType.notification, 5, 6, 7),
        base.Notification(method=5, params=6, kparams=7)
    ),
    (
        (base.MessageType.response, 8, 9, 10),
        base.Response(id=8, result=9, error=10)
    )
]


@pytest.fixture
@patch.multiple(base.BaseProtocol, __abstractmethods__=set())
def protocol():

    return base.BaseProtocol()


@pytest.mark.parametrize("message_tuple,message", test_data)
def test_decode_message(protocol, message_tuple, message):

    assert protocol.decode_message(message_tuple) == message


@pytest.mark.parametrize("message_tuple,message", test_data)
def test_encode_message(protocol, message_tuple, message):

    assert protocol.encode_message(message) == message_tuple


def test_decode_message_unsupported(protocol):

    message_type = int(base.MessageType.invalid)

    with pytest.raises(NotImplementedError) as e:
        protocol.decode_message([message_type])

    assert str(message_type) in str(e.value)


@pytest.mark.parametrize("cls", [base.Request, base.Response])
def test_id_init(cls):

    message = cls(id=None)

    assert isinstance(message.id, uuid.UUID)
