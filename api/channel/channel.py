import json

from api.events.service import Event
from api.travel.service import Travel
from api.libs.channel.channel import Message
from api.libs.representation.pretty import PrettyPrint


class Location:
    def __init__(self, latitude, longitude):
        self.longitude = longitude
        self.latitude = latitude

    def __str__(self):
        return f'{self.latitude},{self.longitude}'


class NotificationMessage(PrettyPrint, Message):
    def __init__(self, user_id: str, travel: Travel, event: Event):
        self.user_id = user_id
        self.travel = travel
        self.event = event

    def serialize(self):
        return json.dumps(dict(
              user_id=self.user_id,
              travel=vars(self.travel),
              event=self.event.to_json(),
          ))

    @classmethod
    def deserialize(cls, raw):
        pass
