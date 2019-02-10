import pickle

from ..goals.models import Goal
from .models import Bike


def bike_list(context):
    try:
        bikes = pickle.load(open("project/bikes/cash/bikes.p", "rb"))
    except:
        bikes = []

    return {
        'bike_list': bikes
    }


def goal_list(context):
    qs = Goal.objects.all()[:3]
    return {'goal_list': qs}
