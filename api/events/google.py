import urllib
import logging
import datetime

from typing import List
from api.token.service import Token
from api.google.client import Client
from api.calendar.service import Calendar
from api.events.service import EventsService, Event


LOG = logging.getLogger(__name__)


class GoogleEventsService(EventsService):
    WEEKS_AHEAD = 4
    RFC3339_TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

    def __init__(self, api_client: Client):
        self.api_client = api_client

    def __time_range(self):
        time_min = datetime.datetime.now()
        time_max = time_min + datetime.timedelta(weeks=self.WEEKS_AHEAD)
        time_min_format = time_min.strftime(self.RFC3339_TIME_FORMAT)
        time_max_format = time_max.strftime(self.RFC3339_TIME_FORMAT)
        return dict(
            timeMin=time_min_format,
            timeMax=time_max_format
        )

    @staticmethod
    def __event_filter(event):
        return event.location and event.location != "None" and event.start_time and event.end_time

    def __filter_events(self, raw_events):
        return list(filter(self.__event_filter, map(lambda e: Event.from_dict(e), raw_events)))

    def fetch(self, token: Token, calendar: Calendar) -> List[Event]:
        params = dict()
        params.update(**self.__time_range())
        calendar_identifier = urllib.parse.quote_plus(calendar.identifier)
        events = self.api_client.get(f'calendar/v3/calendars/{calendar_identifier}/events', token.value, params)
        return self.__filter_events(events.get('items'))
