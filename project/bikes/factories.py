from datetime import date

import factory

from ..users.factories import UserFactory
from .models import Bike, BikeInfo, Component


class BikeFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    date = date(1999, 1, 1)
    full_name = 'Full Name'
    short_name = 'Short Name'

    class Meta:
        model = Bike
        django_get_or_create = ('user', 'short_name',)


class BikeInfoFactory(factory.DjangoModelFactory):
    bike = factory.SubFactory(BikeFactory)
    component = 'Component'
    description = 'Description'

    class Meta:
        model = BikeInfo


class ComponentFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    name = 'Component'

    class Meta:
        model = Component
        django_get_or_create = ('user', 'name',)
