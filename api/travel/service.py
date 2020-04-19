import abc
import collections

from api.libs.representation.pretty import PrettyPrint

Location = collections.namedtuple('Location', ['latitude', 'longitude'])


class Travel(PrettyPrint):
    def __init__(self, duration, routes):
        self.duration = duration
        self.routes = routes


class TravelService(abc.ABC):
    @abc.abstractmethod
    def estimate(self, origin, destination, mode) -> Travel:
        pass
