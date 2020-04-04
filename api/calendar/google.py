from typing import List
import logging

from googleapiclient.discovery import build

from api.calendar.service import CalendarService, Calendar
from api.token.service import Token


LOG = logging.getLogger(__name__)


class GoogleCalendarService(CalendarService):
    @staticmethod
    def map_google_calendars(calendar_list):
        return list(map(lambda calendar: Calendar(identifier=calendar['id']), calendar_list.get(['items'])))

    def fetch(self, token: Token) -> List[Calendar]:
        service = build('calendar', 'v3', credentials=token.value)
        calendar_list = service.calendarList().list()
        LOG.info(calendar_list)
        return self.map_google_calendars(calendar_list)