import pickle

from .models import Bike


def bike_list(context):
    try:
        bikes = pickle.load(open("project/bikes/cash/bikes.p", "rb"))
    except:
        bikes = []

    return {
        'bike_list': bikes
    }


def component_list(context):
    try:
        components = pickle.load(open("project/bikes/cash/components.p", "rb"))
    except:
        components = []

    return {
        'component_list': components
    }    
