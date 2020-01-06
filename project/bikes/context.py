from ..bikes.models import Bike


def bike_list(context):
    bikes = list(Bike.objects.items())

    return {'bike_list': bikes}
