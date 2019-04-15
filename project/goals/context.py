import os
import pickle

from django.conf import settings

from ..goals import signals


def load_cashed_content(name):
    file = os.path.join(settings.CASH_ROOT, name)
    return pickle.load(open(file, "rb"))


def goal_list(context):
    try:
        goals = load_cashed_content('goals.p')
    except:
        signals.cash_goals(None, None)
        goals = load_cashed_content('goals.p')

    return {'goal_list': goals}
