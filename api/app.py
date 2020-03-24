import logging
import pika
from api.callback import callback

logging.basicConfig(level=logging.DEBUG)

HOST_IN = 'rabbit'
EXCHANGE_IN = 'location'
BINDING_KEYS = 'location.*'


def main():
    exchange_in = EXCHANGE_IN
    binding_keys = BINDING_KEYS
    host = HOST_IN

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()

    channel.exchange_declare(exchange=exchange_in, exchange_type='topic')
    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue

    for binding_key in binding_keys:
        channel.queue_bind(exchange=exchange_in, queue=queue_name, routing_key=binding_key)

    print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
