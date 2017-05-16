import enum
from abc import ABCMeta, abstractmethod

from attr import attrib, attributes


class MessageType(enum.IntEnum):
    invalid = 0
    request = 1
    notification = 2
    response = 3


class BaseMessage(metaclass=ABCMeta):
    type = MessageType.invalid


@attributes
class Request:
    type = MessageType.request
    id = attrib()
    method = attrib()
    params = attrib()
    kparams = attrib()


@attributes
class Notification:
    type = MessageType.notification
    method = attrib()
    params = attrib()
    kparams = attrib()


@attributes
class Response:
    type = MessageType.response
    id = attrib()
    result = attrib()
    error = attrib()


BaseMessage.register(Request)
BaseMessage.register(Notification)
BaseMessage.register(Response)


message_type_map = {
    MessageType.request: Request,
    MessageType.notification: Notification,
    MessageType.response: Response,
}


class BaseTransport(metaclass=ABCMeta):

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

        message_ = [getattr(message, attribute.name) for attribute in message.__attrs_attrs__]

        return [message.type] + message_
