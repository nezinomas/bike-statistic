from ..bikes.models import Bike
from .lib.utils import years as Y


def years(context):
    return {'years': Y()[::-1]}


def bike_list(context):
    all_bikes = Bike.objects.items()

    rtn_dict = {
        'bike_list': None,
        'default_bike': None,
    }

    if not all_bikes:
        return rtn_dict


    rtn_dict['bike_list'] = all_bikes
    # Find the default bike, prioritizing the main bike if it exists
    rtn_dict['default_bike'] = next((bike for bike in all_bikes if bike.main), all_bikes[0])

    return rtn_dict