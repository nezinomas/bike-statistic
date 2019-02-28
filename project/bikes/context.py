import os
import pickle

from django.conf import settings


def bike_list(context):
    try:
        f = os.path.join(settings.CASH_ROOT, 'bikes.p')
        bikes = pickle.load(open(f, "rb"))
    except:
        bikes = []

    return {'bike_list': bikes}


def component_list(context):
    try:
        f = os.path.join(settings.CASH_ROOT, 'components.p')
        components = pickle.load(open(f, "rb"))
    except:
        components = []

    return {'component_list': components}
