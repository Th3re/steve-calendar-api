import abc

from api.model.credentials import Credentials


class Store(abc.ABC):
    @abc.abstractmethod
    def save(self, credentials: Credentials):
        pass

    @abc.abstractmethod
    def get(self, user_id) -> Credentials:
        pass
