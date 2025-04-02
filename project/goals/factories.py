import factory

from ..users.factories import UserFactory
from .models import Goal


class GoalFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    year = 2000
    goal = 1000

    class Meta:
        model = Goal
        django_get_or_create = (
            "user",
            "year",
        )
