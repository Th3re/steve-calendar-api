import logging
import datetime

from api.events.service import Event
from api.travel.service import Travel
from api.libs.channel.channel import Channel
from api.channel.channel import NotificationMessage
from api.notification.service import NotificationService


LOG = logging.getLogger(__name__)


class TravelNotificationService(NotificationService):
    def __init__(self, channel: Channel, time_delta):
        self.channel = channel
        self.time_delta = time_delta

    def notify(self, user_id: str, travel: Travel, event: Event):
        message = NotificationMessage(user_id, travel, event)
        start_time = event.start_time
        now = datetime.datetime.now().timestamp()
        time_left = start_time.timestamp() - now
        if time_left - travel.duration < 0:
            LOG.info(f'Not enough time to get to event {event}')
        elif 0 < time_left - travel.duration < self.time_delta:
            response = self.channel.send('', message.serialize())
            LOG.info(f'Notification sent: {response}')
        else:
            LOG.info(f'Too much time to notify event {event}')
