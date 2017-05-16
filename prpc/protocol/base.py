import uuid
import enum
from abc import ABCMeta, abstractmethod

from attr import attrib, attributes, astuple


class MessageType(enum.IntEnum):
    invalid = 0
    request = 1
    notification = 2
    response = 3


class BaseMessage(metaclass=ABCMeta):
    type = MessageType.invalid


def init_id(cls):
    def post_init_(self):
        if self.id == None:
            self.id = uuid.uuid4()

    cls.__attrs_post_init__ = post_init_
    return cls


@attributes
@init_id
class Request:
    type = MessageType.request
    id = attrib(default=None)
    method = attrib(default=None)
    params = attrib(default=tuple())
    kparams = attrib(default=dict())


@attributes
class Notification:
    type = MessageType.notification
    method = attrib(default=None)
    params = attrib(default=tuple())
    kparams = attrib(default=dict())


@attributes
class Response:
    type = MessageType.response
    id = attrib(default=None)
    result = attrib(default=None)
    error = attrib(default=None)


BaseMessage.register(Request)
BaseMessage.register(Notification)
BaseMessage.register(Response)


message_type_map = {
    MessageType.request: Request,
    MessageType.notification: Notification,
    MessageType.response: Response,
}


class BaseProtocol(metaclass=ABCMeta):

    @abstractmethod
    def feed(self, data):
        """unpack raw data into individual message tuples

        Args:
            data: stream of arbitrary bytes

        Returns:
            generator of zero or more messages
        """

        pass  # pragma nocover

    @abstractmethod
    def pack(self, message):
        """pack message tuple into protocol message

        Args:
            message: concrete BaseMessage instance

        Returns:
            serialized message
        """

        pass  # pragma nocover

    def decode_message(self, message_tuple):
        """unpack message tuple into a message object

        Args:
            message: tuple

        Returns:
            concrete BaseMessage instance
        """

        message_type, *message_ = message_tuple

        if message_type not in message_type_map:
            raise NotImplementedError('unsupported message type: {message_type}'.format(message_type=message_type))

        cls = message_type_map[message_type]
        return cls(*message_)

    def encode_message(self, message):
        """pack message object into a message tuple

        Args:
            message: concrete BaseMessage

        Returns:
            message tuple
        """

        return (message.type,) + astuple(message)
