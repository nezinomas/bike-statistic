import os
import pickle

from django.conf import settings

from .models import Goal


def goal_list(context):
    try:
        f = os.path.join(settings.CASH_ROOT, 'goals.p')
        goals = pickle.load(open(f, "rb"))
    except:
        goals = []

    return {
        'goal_list': goals
    }
