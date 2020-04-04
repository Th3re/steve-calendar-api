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
from api.environment import read_environment


logging.basicConfig(level=logging.INFO)

LOG = logging.getLogger(__name__)

env = read_environment()

token_service = SteveTokenService(env.auth.url)
calendar_service = GoogleCalendarService()
event_service = GoogleEventsService()
travel_service = GoogleTravelService()
rabbit_connection = create_connection(
    env.rabbit.host_out,
    env.rabbit.port_out,
    env.rabbit.connection_attempts,
    env.rabbit.retry_delay
)
rabbit_channel = create_rabbit_channel(rabbit_connection, env.rabbit.exchange_out, env.rabbit.topic_out)
notification_service = TravelNotificationService(rabbit_channel)


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
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=env.rabbit.host_in))
    connection_channel = connection.channel()

    connection_channel.exchange_declare(exchange=env.rabbit.exchange_in, exchange_type='topic')
    result = connection_channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue

    connection_channel.queue_bind(exchange=env.rabbit.exchange_in, queue=queue_name, routing_key=env.rabbit.binding_key_in)

    LOG.info(' [*] Waiting for messages. To exit press CTRL+C')

    connection_channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    connection_channel.start_consuming()
