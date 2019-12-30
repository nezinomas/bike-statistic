from datetime import date

import factory

from ..users.factories import UserFactory
from .models import Bike, BikeInfo


class BikeFactory(factory.DjangoModelFactory):
    class Meta:
        model = Bike
        django_get_or_create = ('user',)

    user = factory.SubFactory(UserFactory)
    date = date(1999, 1, 1)
    full_name = 'Full Name'
    short_name = 'Short Name'


class BikeInfoFactory(factory.DjangoModelFactory):
    class Meta:
        model = BikeInfo
        django_get_or_create = ('bike',)

    bike = factory.SubFactory(BikeFactory)
    component = 'Component'
    description = 'Description'
