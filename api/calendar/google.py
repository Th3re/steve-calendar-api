import logging

from typing import List
from api.token.service import Token
from api.calendar.service import CalendarService, Calendar


LOG = logging.getLogger(__name__)


class GoogleCalendarService(CalendarService):
    def __init__(self, api_client):
        self.api_client = api_client

    @staticmethod
    def __retrieve_identifiers(calendars):
        return list(map(lambda calendar: Calendar(identifier=calendar['id']), calendars.get('items')))

    def fetch(self, token: Token) -> List[Calendar]:
        calendars = self.api_client.get('calendar/v3/users/me/calendarList', token.value)
        return self.__retrieve_identifiers(calendars)
