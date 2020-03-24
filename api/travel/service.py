import abc
import collections

Location = collections.namedtuple('Location', ['latitude', 'longitude'])


class Travel:
    def __init__(self, duration, steps):
        self.duration = duration
        self.steps = steps


class TravelService(abc.ABC):
    @abc.abstractmethod
    def estimate(self, origin, destination, mode) -> Travel:
        pass
