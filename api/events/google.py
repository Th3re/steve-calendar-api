from typing import List

from api.calendar.service import Calendar
from api.events.service import EventsService, Event
from api.token.service import Token


class GoogleEventsService(EventsService):
    def fetch(self, token: Token, calendar: Calendar) -> List[Event]:
        return [Event(1,2,3,4,5,6,7)]