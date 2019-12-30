from datetime import date

import factory

from ..users.factories import UserFactory
from .models import Bike, BikeInfo


class BikeFactory(factory.DjangoModelFactory):
    class Meta:
        model = Bike

    user = factory.SubFactory(UserFactory)
    date = date(1999, 1, 1)
    full_name = 'Full Name'
    short_name = 'Short Name'
