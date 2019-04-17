from factory import DjangoModelFactory

from .models import Goal


class GoalFactory(DjangoModelFactory):
    class Meta:
        model = Goal

    year = 2000
    goal = 1000
