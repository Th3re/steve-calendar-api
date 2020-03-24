import logging

from api.calendar.google import GoogleCalendarService
from api.channel.rabbit import create_connection, create_rabbit_channel
from api.events.google import GoogleEventsService
from api.notification.travel import TravelNotificationService
from api.token.steve import SteveTokenService
from api.travel.google import GoogleTravelService
from api.travel.service import Location


LOG = logging.getLogger(__name__)

RABBIT_HOST_OUT = 'localhost'
RABBIT_PORT_OUT = '5672'
RABBIT_CONNECTION_ATTEMPTS = 10
RABBIT_RETRY_DELAY = 3
EXCHANGE_OUT = ''
TOPIC = 'travel'

token_service = SteveTokenService()
calendar_service = GoogleCalendarService()
event_service = GoogleEventsService()
travel_service = GoogleTravelService()
rabbit_connection = create_connection(
    RABBIT_HOST_OUT,
    RABBIT_PORT_OUT,
    RABBIT_CONNECTION_ATTEMPTS,
    RABBIT_RETRY_DELAY
)
channel = create_rabbit_channel(rabbit_connection, EXCHANGE_OUT, TOPIC)
notification_service = TravelNotificationService(channel)


def callback(ch, method, properties, body):
    LOG.debug(" [x] %r:%r" % (method.routing_key, body))
    _, user_id = method.routing_key.split('.')
    location = Location(latitude=body['latitude'], longitde=body['longitude'])
    token = token_service.fetch(user_id)
    calendars = calendar_service.fetch(token)
    for calendar in calendars:
        events = event_service.fetch(token, calendar)
        for event in events:
            travel = travel_service.estimate(location, event.location, mode='driving')
            notification_service.notify(travel, event)
