import abc

from typing import List
from api.token.service import Token
from api.model.representation import PrettyPrint


class Calendar(PrettyPrint):
    def __init__(self, identifier):
        self.identifier = identifier


class CalendarService(abc.ABC):
    @abc.abstractmethod
    def fetch(self, token: Token) -> List[Calendar]:
        pass
