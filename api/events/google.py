import urllib
import logging

from typing import List
from api.token.service import Token
from api.google.client import Client
from api.calendar.service import Calendar
from api.events.service import EventsService, Event


LOG = logging.getLogger(__name__)


class GoogleEventsService(EventsService):
    def __init__(self, api_client: Client):
        self.api_client = api_client

    def fetch(self, token: Token, calendar: Calendar) -> List[Event]:
        calendar_identifier = urllib.parse.quote_plus(calendar.identifier)
        events = self.api_client.get(f'calendar/v3/calendars/{calendar_identifier}/events', token.value)
        return [Event.from_dict(event) for event in events.get('items')]
