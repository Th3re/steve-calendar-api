from api.libs.environment.environmentreader import EnvironmentReader
from api.libs.representation.pretty import PrettyPrint


class Rabbit(EnvironmentReader):
    def __init__(self):
        super()
        self.topic_out = self.get('topic_out')
        self.retry_delay = int(self.get('retry_delay'))
        self.connection_attempts = int(self.get('connection_attempts'))
        self.port_out = int(self.get('port_out'))
        self.host_out = self.get('host_out')
        self.binding_key_in = self.get('binding_key_in')
        self.exchange_in = self.get('exchange_in')
        self.host_in = self.get('host_in')
        self.exchange_out = self.get('exchange_out')


class Google(EnvironmentReader):
    def __init__(self):
        super()
        self.host = self.get('host')
        self.apikey = self.get('apikey')
        self.maps_host = self.get('maps_host')


class Auth(EnvironmentReader):
    def __init__(self):
        super()
        self.url = self.get('url')


class Time(EnvironmentReader):
    def __init__(self):
        super()
        self.delta = float(self.get('delta'))


class Environment(PrettyPrint):
    def __init__(self):
        self.google = Google()
        self.rabbit = Rabbit()
        self.auth = Auth()
        self.time = Time()

    @staticmethod
    def read():
        return Environment()
