import json
import pika
import logging
import traceback

from api.libs.cache.memory import MemoryAccessCache
from api.steve.events import EventsAPIClient
from api.travel.service import Location
from api.environment import Environment
from api.token.steve import SteveTokenService
from api.travel.google import GoogleTravelService
from api.libs.google.google_client import GoogleClient
from api.events.google import GoogleEventsService
from api.calendar.google import GoogleCalendarService
from api.libs.channel.rabbit.channel import RabbitChannel
from api.notification.travel import TravelNotificationService
from api.libs.channel.rabbit.environment import ChannelEnvironment, RabbitEnvironment


logging.basicConfig(level=logging.INFO)

LOG = logging.getLogger(__name__)

env = Environment.read()

client = GoogleClient(env.google.host)
maps_client = GoogleClient(env.google.maps_host)
token_service = SteveTokenService(env.auth.url)
calendar_service = GoogleCalendarService(client)
event_service = GoogleEventsService(client)
travel_service = GoogleTravelService(maps_client, env.google.apikey)
rabbit_channel = RabbitChannel.create(ChannelEnvironment(env.rabbit.exchange_out, env.rabbit.topic_out),
                                      RabbitEnvironment(env.rabbit.host_out,
                                                        env.rabbit.port_out,
                                                        env.rabbit.connection_attempts,
                                                        env.rabbit.retry_delay))
notification_service = TravelNotificationService(rabbit_channel, env.time.delta, MemoryAccessCache())
steve_events_client = EventsAPIClient(env.steve.events_url)


def callback(_, method, __, body):
    try:
        payload = json.loads(body)
        LOG.info(" [x] %r:%r" % (method.routing_key, payload))
        _, user_id = method.routing_key.split('.')
        location = Location(latitude=payload['latitude'], longitude=payload['longitude'])
        token = token_service.fetch(user_id)
        calendars = calendar_service.fetch(token)
        all_events = []
        for calendar in calendars:
            LOG.info(f'Calendar: {calendar}')
            events = event_service.fetch(token, calendar)
            all_events.extend(events)
            for event in events:
                LOG.info(f'Event: {event}')
                travel = travel_service.estimate(location, event.location, mode='driving')
                if travel:
                    notification_service.notify(user_id, travel, event)
                else:
                    LOG.error(f'Could not find a way from {location} to {event.location}')
        steve_events_client.store(user_id, all_events)
    except Exception as e:
        LOG.error(f'{repr(e)}, {traceback.format_exc()}')


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
