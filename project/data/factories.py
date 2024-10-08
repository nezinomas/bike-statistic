from datetime import datetime, timedelta, timezone

import factory

from ..bikes.factories import BikeFactory
from ..users.factories import UserFactory
from .models import Data


class DataFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    bike = factory.SubFactory(BikeFactory)
    date = datetime(2000, 1, 1, 3, 2, 1, tzinfo=timezone.utc)
    distance = 10
    time = timedelta(seconds=(1000))
    ascent = 100
    max_speed = 15
    cadence = 85
    heart_rate = 140
    temperature = 10

    class Meta:
        model = Data
