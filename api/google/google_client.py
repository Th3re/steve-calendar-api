import requests

from api.google.client import Client
from api.exceptions.connectivity import AuthenticationError, UnknownConnectivityError


class GoogleClient(Client):
    def __init__(self, host):
        self.host = host

    def get(self, endpoint, token):
        response = requests.get(f'{self.host}/{endpoint}', headers={'Authorization': f'Bearer {token}'})
        if 200 <= response.status_code < 300:
            return response.json()
        if response.status_code == 401:
            raise AuthenticationError(response)
        else:
            raise UnknownConnectivityError(response)