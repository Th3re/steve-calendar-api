import json
import logging
import pika.exceptions

from api.channel.channel import Channel, NotificationMessage, ChannelResponse

LOG = logging.getLogger(__name__)


def create_connection(host, port, connection_attempts, retry_delay):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port,
                                                                   connection_attempts=connection_attempts,
                                                                   retry_delay=retry_delay))
    return connection.channel()


def create_rabbit_channel(channel, exchange, topic):
    rabbit_channel = RabbitChannel(channel, exchange=exchange, topic=topic)
    return rabbit_channel


class RabbitChannel(Channel):
    __exchange_type = 'topic'

    def __init__(self, channel, exchange, topic):
        self.channel = channel
        self.exchange = exchange
        self.topic = topic

    @staticmethod
    def __serialize_message(message: NotificationMessage):
        return json.dumps(dict(
            user_id=message.user_id,
            travel=vars(message.travel),
            event=message.event.to_json(),
        ))

    def send(self, message: NotificationMessage) -> ChannelResponse:
        try:
            self.channel.queue_declare(queue=self.topic, durable=True)
        except pika.exceptions.AMQPError as amqp_error:
            LOG.error(amqp_error)
            return ChannelResponse(
                message=f"Cannot declare exchange {self.exchange} of type {self.__exchange_type}",
                status=ChannelResponse.Status.ERROR,
            )
        routing_key = self.topic
        body = self.__serialize_message(message)
        try:
            self.channel.basic_publish(
                exchange=self.exchange,
                routing_key=routing_key,
                body=body,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                )
            )
        except pika.exceptions.AMQPError as amqp_error:
            LOG.error(amqp_error)
            return ChannelResponse(
                message=f"Cannot publish message to {routing_key}",
                status=ChannelResponse.Status.ERROR,
            )
        return ChannelResponse(
            message=f"Notification uploaded",
            status=ChannelResponse.Status.OK,
        )
