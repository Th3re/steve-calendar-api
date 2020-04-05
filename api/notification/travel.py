import logging

from api.events.service import Event
from api.travel.service import Travel
from api.notification.service import NotificationService
from api.channel.channel import Channel, NotificationMessage


LOG = logging.getLogger(__name__)


class TravelNotificationService(NotificationService):
    def __init__(self, channel: Channel):
        self.channel = channel

    def notify(self, travel: Travel, event: Event):
        message = NotificationMessage(travel, event)
        response = self.channel.send(message)
        LOG.debug(response)
