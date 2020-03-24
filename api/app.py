import logging
import pika
import json
from api.calendar.google import GoogleCalendarService
from api.channel.rabbit import create_connection, create_rabbit_channel
from api.events.google import GoogleEventsService
from api.notification.travel import TravelNotificationService
from api.token.steve import SteveTokenService
from api.travel.google import GoogleTravelService
from api.travel.service import Location


logging.basicConfig(level=logging.INFO)

HOST_IN = 'rabbit'
EXCHANGE_IN = 'location'
BINDING_KEY = 'location.*'

LOG = logging.getLogger(__name__)

RABBIT_HOST_OUT = 'rabbit'
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
    payload = json.loads(body)
    LOG.info(" [x] %r:%r" % (method.routing_key, payload))
    _, user_id = method.routing_key.split('.')
    location = Location(latitude=payload['latitude'], longitude=payload['longitude'])
    token = token_service.fetch(user_id)
    calendars = calendar_service.fetch(token)
    for calendar in calendars:
        events = event_service.fetch(token, calendar)
        for event in events:
            travel = travel_service.estimate(location, event.location, mode='driving')
            notification_service.notify(travel, event)


def main():
    exchange_in = EXCHANGE_IN
    host = HOST_IN

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()

    channel.exchange_declare(exchange=exchange_in, exchange_type='topic')
    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue

    binding_key = BINDING_KEY
    channel.queue_bind(exchange=exchange_in, queue=queue_name, routing_key=binding_key)

    LOG.info(' [*] Waiting for messages. To exit press CTRL+C')

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
