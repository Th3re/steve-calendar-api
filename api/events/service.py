import abc

from typing import List
from api.token.service import Token
from api.calendar.service import Calendar
from api.libs.events import Event


class EventsService(abc.ABC):
    @abc.abstractmethod
    def fetch(self, token: Token, calendar: Calendar) -> List[Event]:
        pass
