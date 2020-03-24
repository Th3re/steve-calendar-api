import abc


class Token:
    def __init__(self, value):
        self.value = value


class TokenService(abc.ABC):
    @abc.abstractmethod
    def fetch(self, user_id: str) -> Token:
        pass
