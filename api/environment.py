import os


class EnvClass:
    def get(self, name: str) -> str:
        env_name = f'{self.__class__.__name__.upper()}_{name.upper()}'
        return os.environ[env_name]

    def __repr__(self):
        return ' '.join([f'{self.__class__.__name__.upper()}_{name.upper()}: {value}'
                         for name, value in self.__dict__.items()])


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
        self.client_id = self.get('client_id')
        self.client_secret = self.get('client_secret')


class Auth(EnvClass):
    def __init__(self):
        super()
        self.url = self.get('url')


class Environment(EnvClass):
    def __init__(self):
        self.google_credentials = Google()
        self.rabbit = Rabbit()


def read_environment() -> Environment:
    return Environment()
