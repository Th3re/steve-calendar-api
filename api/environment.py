import os


class Rabbit:
    HOST_IN = 'RABBIT_HOST_IN'
    EXCHANGE_IN = 'RABBIT_EXCHANGE_IN'
    BINDING_KEY_IN = 'RABBIT_BINDING_KEY_IN'
    HOST_OUT = 'RABBIT_HOST_OUT'
    PORT_OUT = 'RABBIT_PORT_OUT'
    CONNECTION_ATTEMPTS = 'RABBIT_CONNECTION_ATTEMPTS'
    RETRY_DELAY = 'RABBIT_RETRY_DELAY'
    EXCHANGE_OUT = 'RABBIT_EXCHANGE_OUT'
    TOPIC_OUT = 'RABBIT_TOPIC_OUT'

    def __init__(self, host_in, exchange_in, binding_key_in, host_out,
                 port_out, connection_attempts, retry_delay, topic_out, exchange_out):
        self.topic_out = topic_out
        self.retry_delay = retry_delay
        self.connection_attempts = connection_attempts
        self.port_out = port_out
        self.host_out = host_out
        self.binding_key_in = binding_key_in
        self.exchange_in = exchange_in
        self.host_in = host_in
        self.exchange_out = exchange_out

    def __repr__(self):
        return f'HOST_IN: {self.host_in} EXCHANGE_IN: {self.exchange_in} BINDING_KEY_IN: {self.binding_key_in} ' \
               f'HOST_OUT {self.host_out} PORT_OUT: {self.port_out} CONNECTION_ATTEMPTS: {self.connection_attempts} ' \
               f'RETRY_DELAY: {self.retry_delay} TOPIC_OUT: {self.topic_out} EXCHANGE_OUT: {self.exchange_out}'


class Google:
    CLIENT_ID = 'CLIENT_ID'
    CLIENT_SECRET = 'CLIENT_SECRET'

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def __repr__(self):
        return f'CLIENT_ID: {self.client_id} CLIENT_SECRET: {self.client_secret}'


class Environment:

    def __init__(self, google_credentials: Google, rabbit: Rabbit):
        self.google_credentials = google_credentials
        self.rabbit = rabbit

    def __repr__(self):
        return f'GOOGLE_CREDENTIALS: [{self.google_credentials}] RABBIT [{self.rabbit}]'


def read_environment() -> Environment:
    return Environment(google_credentials=Google(client_id=os.environ[Google.CLIENT_ID],
                                                 client_secret=os.environ[Google.CLIENT_SECRET]),
                       rabbit=Rabbit(host_in=os.environ[Rabbit.HOST_IN],
                                     exchange_in=os.environ[Rabbit.EXCHANGE_IN],
                                     binding_key_in=os.environ[Rabbit.BINDING_KEY_IN],
                                     host_out=os.environ[Rabbit.HOST_OUT],
                                     port_out=os.environ[Rabbit.PORT_OUT],
                                     connection_attempts=int(os.environ[Rabbit.CONNECTION_ATTEMPTS]),
                                     retry_delay=int(os.environ[Rabbit.RETRY_DELAY]),
                                     topic_out=os.environ[Rabbit.TOPIC_OUT],
                                     exchange_out=os.environ[Rabbit.EXCHANGE_OUT]))
