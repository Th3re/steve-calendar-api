from typing import List

from api.calendar.service import Calendar
from api.events.service import EventsService, Event
from api.token.service import Token


class GoogleEventsService(EventsService):
    def fetch(self, token: Token, calendar: Calendar) -> List[Event]:
        return [Event(identifier='123123')]