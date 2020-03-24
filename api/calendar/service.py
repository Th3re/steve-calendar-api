import abc
from typing import List

from api.token.service import Token


class Calendar:
    def __init__(self, identifier):
        self.identifier = identifier


class CalendarService(abc.ABC):
    @abc.abstractmethod
    def fetch(self, token: Token) -> List[Calendar]:
        pass
