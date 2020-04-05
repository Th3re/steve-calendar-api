import requests


class APIError(Exception):
    def __init__(self, response: requests.Response):
        self.response = response

    def __repr__(self):
        return f'<{self.__class__.__name__}>[status_code: \"{self.response.status_code}\", content: \"{self.response.content}\"]'


class AuthenticationError(APIError):
    pass


class UnknownConnectivityError(APIError):
    pass
