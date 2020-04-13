import os

from api.model.representation import EnvPrint


class EnvClass(EnvPrint):
    def get(self, name: str) -> str:
        env_name = f'{self.__class__.__name__.upper()}_{name.upper()}'
        return os.environ[env_name]


class Rabbit(EnvClass):
    def __init__(self):
        super()
        self.topic_out = self.get('topic_out')
        self.retry_delay = int(self.get('retry_delay'))
        self.connection_attempts = int(self.get('connection_attempts'))
        self.port_out = self.get('port_out')
        self.host_out = self.get('host_out')
        self.binding_key_in = self.get('binding_key_in')
        self.exchange_in = self.get('exchange_in')
        self.host_in = self.get('host_in')
        self.exchange_out = self.get('exchange_out')


class Google(EnvClass):
    def __init__(self):
        super()
        self.host = self.get('host')
        self.apikey = self.get('apikey')
        self.maps_host = self.get('maps_host')


class Auth(EnvClass):
    def __init__(self):
        super()
        self.url = self.get('url')


class Time(EnvClass):
    def __init__(self):
        super()
        self.delta = float(self.get('delta'))


class Environment(EnvClass):
    def __init__(self):
        self.google = Google()
        self.rabbit = Rabbit()
        self.auth = Auth()
        self.time = Time()


def read_environment() -> Environment:
    return Environment()
