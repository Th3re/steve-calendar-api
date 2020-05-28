import abc

from typing import List

from api.libs.events.event import Event
from api.token.service import Token
from api.calendar.service import Calendar


class EventsService(abc.ABC):
    @abc.abstractmethod
    def fetch(self, token: Token, calendar: Calendar) -> List[Event]:
        pass
