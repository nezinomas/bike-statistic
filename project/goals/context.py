import pickle

from .models import Goal


def goal_list(context):
    try:
        goals = pickle.load(open("project/goals/cash/goals.p", "rb"))
    except:
        goals = []

    return {
        'goal_list': goals
    }
