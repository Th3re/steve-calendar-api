import abc
import copy
import datetime

from typing import List, Optional
from api.token.service import Token
from api.calendar.service import Calendar
from api.libs.representation.pretty import PrettyPrint


class Event(PrettyPrint):
    def __init__(self,
                 identifier: str,
                 html_link: str,
                 summary: str,
                 location: Optional[str],
                 start_time: datetime,
                 end_time: datetime,
                 status: Optional[str]):
        self.status = status
        self.end_time = end_time
        self.start_time = start_time
        self.location = location
        self.summary = summary
        self.html_link = html_link
        self.identifier = identifier

    @staticmethod
    def __parse_time(time_string):
        # Example time_string 2020-04-23T16:30:00+02:00
        timestamp = time_string.get('dateTime')
        if not timestamp:
            return None
        return datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S%z')

    def to_json(self):
        body = copy.copy(vars(self))
        format = '%Y-%m-%dT%H:%M:%S%z'
        body['start_time'] = datetime.datetime.strftime(self.start_time, format)
        body['end_time'] = datetime.datetime.strftime(self.end_time, format)
        return body

    @staticmethod
    def from_dict(dictionary):
        start_time = Event.__parse_time(dictionary['start'])
        end_time = Event.__parse_time(dictionary['end'])
        return Event(identifier=dictionary['id'],
                     html_link=dictionary['htmlLink'],
                     summary=dictionary['summary'],
                     location=dictionary.get('location'),
                     start_time=start_time,
                     end_time=end_time,
                     status=dictionary.get('status'))


class EventsService(abc.ABC):
    @abc.abstractmethod
    def fetch(self, token: Token, calendar: Calendar) -> List[Event]:
        pass
