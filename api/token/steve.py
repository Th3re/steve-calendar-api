import logging
import requests

from api.token.service import TokenService, Token


LOG = logging.getLogger(__name__)


class SteveTokenService(TokenService):
    def __init__(self, auth_url):
        self.auth_url = auth_url

    def fetch(self, user_id: str) -> Token:
        response = requests.get(f'{self.auth_url}/token/{user_id}').json()
        token = response['token']
        code = response['code']
        message = response['message']
        LOG.debug(f'Code: {code}, Message: {message}')
        return Token(value=token)
