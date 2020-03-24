from typing import List

from api.calendar.service import CalendarService, Calendar
from api.token.service import Token


class GoogleCalendarService(CalendarService):
    def fetch(self, token: Token) -> List[Calendar]:
        return [Calendar(identifier="123")]