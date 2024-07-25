from ..bikes.models import Bike
from .lib.utils import years as Y


def years(context):
    return {'years': Y()[::-1]}


def bike_list(context):
    all_bikes = Bike.objects.items()

    # Find the default bike, prioritizing the main bike if it exists
    default_bike = next((bike for bike in all_bikes if bike.main), all_bikes[0])

    return {
        'bike_list': all_bikes,
        'default_bike': default_bike,
    }