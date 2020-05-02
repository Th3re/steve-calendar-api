import requests
import logging
from http import HTTPStatus

LOG = logging.getLogger(__name__)


class EventsAPIClient:
    def __init__(self, api_url):
        self.api_url = api_url

    def store(self, identifier, events):
        payload = dict(
            userId=identifier,
            events=events
        )
        response = requests.post(f'{self.api_url}/store', json=payload)
        LOG.info(response)
        if response.status_code != HTTPStatus.OK:
            raise ConnectionError("Cannot store events")
