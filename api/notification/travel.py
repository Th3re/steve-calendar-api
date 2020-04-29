import logging
import datetime

from api.events.service import Event
from api.libs.cache.cache import Cache
from api.travel.service import Travel
from api.libs.channel.channel import Channel
from api.channel.channel import NotificationMessage
from api.notification.service import NotificationService


LOG = logging.getLogger(__name__)


class TravelNotificationService(NotificationService):
    def __init__(self, channel: Channel, time_delta, cache: Cache):
        self.channel = channel
        self.time_delta = time_delta
        self.cache = cache

    def notify(self, user_id: str, travel: Travel, event: Event):
        message = NotificationMessage(user_id, travel, event)
        start_time = event.start_time
        now = datetime.datetime.now().timestamp()
        time_left = start_time.timestamp() - now
        time_to_leave = time_left - travel.duration
        if time_to_leave < 0:
            LOG.info(f'Not enough time to get to event {event.identifier}')
        elif 0 < time_to_leave < self.time_delta:
            event_id = self.cache.get(event.identifier)
            if event_id:
                LOG.info(f'Event already sent {event.identifier}')
                return
            notification_time = datetime.datetime.now()
            self.cache.set(event.identifier, notification_time, time_to_leave)
            response = self.channel.send('', message.serialize())
            LOG.info(f'Notification sent: {response} for event {event}')
        else:
            LOG.info(f'Too much time to notify event {event.identifier}')
