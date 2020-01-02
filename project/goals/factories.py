from factory import DjangoModelFactory, SubFactory

from ..users.factories import UserFactory
from .models import Goal


class GoalFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    year = 2000
    goal = 1000

    class Meta:
        model = Goal
        django_get_or_create = ('user', 'year',)
