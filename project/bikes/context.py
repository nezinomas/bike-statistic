from .models import Bike
from ..goals.models import Goal


def bike_list(context):
    q = Bike.objects.all()
    return {'bike_list': q}


def goal_list(context):
    qs = Goal.objects.all()[:3]
    return {'goal_list': qs}
