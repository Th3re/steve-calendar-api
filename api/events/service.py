import abc
from typing import List

from api.calendar.service import Calendar
from api.token.service import Token


class Event:
    def __init__(self, identifier, html_link, summary, location, start_time, end_time, status):
        self.status = status
        self.end_time = end_time
        self.start_time = start_time
        self.location = location
        self.summary = summary
        self.html_link = html_link
        self.identifier = identifier


class EventsService(abc.ABC):
    @abc.abstractmethod
    def fetch(self, token: Token, calendar: Calendar) -> List[Event]:
        pass
