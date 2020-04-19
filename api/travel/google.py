import logging
import urllib
from typing import Optional

from api.travel.service import TravelService, Travel

LOG = logging.getLogger(__name__)


class GoogleTravelService(TravelService):
    def __init__(self, api_client, api_key):
        self.api_key = api_key
        self.api_client = api_client

    def estimate(self, origin, destination, mode) -> Optional[Travel]:
        params = dict(
            origin=f'{origin.latitude},{origin.longitude}',
            destination=urllib.parse.quote_plus(destination),
            key=self.api_key
        )
        # default mode: DRIVING
        response = self.api_client.get('maps/api/directions/json', '', params)
        if response.get('status') != "OK":
            LOG.error(f'Could not retrieve travel data, response: {response}')
            return None
        route = response['routes'][0]
        duration = route['legs'][0]['duration']['value']
        return Travel(duration=duration, routes=route)
