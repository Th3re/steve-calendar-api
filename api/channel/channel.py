import abc
import enum

from api.events.service import Event
from api.travel.service import Travel
from api.model.representation import PrettyPrint


class Location:
    def __init__(self, latitude, longitude):
        self.longitude = longitude
        self.latitude = latitude

    def __str__(self):
        return f'{self.latitude},{self.longitude}'


class NotificationMessage(PrettyPrint):
    def __init__(self, user_id: str, travel: Travel, event: Event):
        self.user_id = user_id
        self.travel = travel
        self.event = event


class ChannelResponse(PrettyPrint):
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
