from datetime import date

import factory

from ..users.factories import UserFactory
from .models import Bike, BikeInfo, Component, ComponentStatistic


class BikeFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    date = date(1999, 1, 1)
    full_name = 'Full Name'
    short_name = 'Short Name'
    main = False
    retired = False

    class Meta:
        model = Bike
        django_get_or_create = ('user', 'short_name',)


class BikeInfoFactory(factory.django.DjangoModelFactory):
    bike = factory.SubFactory(BikeFactory)
    component = 'Component'
    description = 'Description'

    class Meta:
        model = BikeInfo


class ComponentFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    name = 'Component'

    class Meta:
        model = Component
        django_get_or_create = ('user', 'name',)


class ComponentStatisticFactory(factory.django.DjangoModelFactory):
    start_date = date(1999, 1, 1)
    end_date = date(1999, 1, 31)
    price = 1.11
    brand = 'Brand'
    bike = factory.SubFactory(BikeFactory)
    component = factory.SubFactory(ComponentFactory)

    class Meta:
        model = ComponentStatistic
