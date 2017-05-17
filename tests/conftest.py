from unittest import mock

import pytest


@pytest.fixture
def buf():
    return []


@pytest.fixture
def transport(buf):
    transport = mock.Mock()

    def write(chunk):
        buf.append(chunk)

    transport.write.side_effect = write

    return transport
