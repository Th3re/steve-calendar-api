import abc

from api.events.service import Event
from api.travel.service import Travel


class NotificationService(abc.ABC):
    @abc.abstractmethod
    def notify(self, travel: Travel, event: Event):
        pass
