import os
import pickle

from django.conf import settings

from ..bikes.models import Bike, Component


def load_cashed_content(name):
    file = os.path.join(settings.CASH_ROOT, name)
    return pickle.load(open(file, "rb"))


def bike_list(context):
    bikes = list(Bike.objects.all().values())

    return {'bike_list': bikes}
