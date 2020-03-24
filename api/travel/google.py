from api.travel.service import TravelService, Travel


class GoogleTravelService(TravelService):
    def estimate(self, origin, destination, mode) -> Travel:
        return Travel(duration=3600, steps=None)
