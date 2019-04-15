import os
import pickle

from django.conf import settings

from ..bikes import signals


def load_cashed_content(name):
    file = os.path.join(settings.CASH_ROOT, name)
    return pickle.load(open(file, "rb"))


def bike_list(context):
    try:
        bikes = load_cashed_content('bikes.p')
    except:
        signals.cash_bikes(None, None)
        bikes = load_cashed_content('bikes.p')

    return {'bike_list': bikes}


def component_list(context):
    try:
        components = load_cashed_content('components.p')
    except:
        signals.cash_components(None, None)
        components = load_cashed_content('components.p')

    return {'component_list': components}
