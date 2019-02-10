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
