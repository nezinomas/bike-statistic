from ..bikes.models import Bike
from ..core.lib import utils


def bike_list(context):
    user = utils.get_user()

    # AnonymousUser don't have id
    if user.id:
        bikes = list(Bike.objects.items())
    else:
        bikes = None

    return {'bike_list': bikes}
