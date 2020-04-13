import logging

from typing import List
from api.token.service import Token
from api.calendar.service import CalendarService, Calendar

LOG = logging.getLogger(__name__)


class GoogleCalendarService(CalendarService):
    IGNORED_CALENDARS = {'addressbook#contacts@group.v.calendar.google.com',
                         'en.polish#holiday@group.v.calendar.google.com'}

    def __init__(self, api_client):
        self.api_client = api_client

    def __retrieve_identifiers(self, calendars):
        return list(filter(lambda x: x not in self.IGNORED_CALENDARS,
                           map(lambda calendar: Calendar(identifier=calendar['id']), calendars.get('items'))))

    def fetch(self, token: Token) -> List[Calendar]:
        calendars = self.api_client.get('calendar/v3/users/me/calendarList', token.value)
        return self.__retrieve_identifiers(calendars)
