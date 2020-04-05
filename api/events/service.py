import abc

from typing import List, Optional
from api.token.service import Token
from api.calendar.service import Calendar
from api.model.representation import PrettyPrint


class Event(PrettyPrint):
    def __init__(self,
                 identifier: str,
                 html_link: str,
                 summary: str,
                 location: Optional[str],
                 start_time: str,
                 end_time: str,
                 status: Optional[str]):
        self.status = status
        self.end_time = end_time
        self.start_time = start_time
        self.location = location
        self.summary = summary
        self.html_link = html_link
        self.identifier = identifier

    @staticmethod
    def from_dict(dictionary):
        return Event(identifier=dictionary['id'],
                     html_link=dictionary['htmlLink'],
                     summary=dictionary['summary'],
                     location=dictionary.get('location'),
                     start_time=dictionary['start'],
                     end_time=dictionary['end'],
                     status=dictionary.get('status'))


class EventsService(abc.ABC):
    @abc.abstractmethod
    def fetch(self, token: Token, calendar: Calendar) -> List[Event]:
        pass
