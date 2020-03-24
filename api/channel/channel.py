import abc
import enum
from collections import namedtuple

from api.events.service import Event
from api.travel.service import Travel

Location = namedtuple("Location", ["latitude", "longitude"])


class NotificationMessage:
    def __init__(self, travel: Travel, event: Event):
        self.travel = travel
        self.event = event


class ChannelResponse:
    class Status(enum.Enum):
        OK = "OK"
        ERROR = "ERROR"

    def __init__(self, message: str, status: Status):
        self.message = message
        self.status = status


class Channel(abc.ABC):
    @abc.abstractmethod
    def send(self, message: NotificationMessage) -> ChannelResponse:
        pass
