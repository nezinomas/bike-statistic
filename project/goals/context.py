import os
import pickle

from django.conf import settings

from ..goals.models import Goal


def load_cashed_content(name):
    file = os.path.join(settings.CASH_ROOT, name)
    return pickle.load(open(file, "rb"))


def goal_list(context):
    goals = list(Goal.objects.all().values())

    return {'goal_list': goals}
