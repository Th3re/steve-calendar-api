import abc


class Client(abc.ABC):
    @abc.abstractmethod
    def get(self, endpoint, token):
        pass
