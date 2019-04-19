from datetime import datetime, timedelta

import factory
from django.contrib.auth.models import User

from ..bikes.models import Bike, Component, ComponentStatistic
from ..reports.models import Data


class BikeFactory(factory.DjangoModelFactory):
    class Meta:
        model = Bike
        django_get_or_create = ('full_name', 'short_name', 'date')

    full_name = 'bike'
    short_name = 'bike'
    slug = 'bike'
    date = datetime(1970, 1, 1).date()


class ComponentFactory(factory.DjangoModelFactory):
    class Meta:
        model = Component
        django_get_or_create = ('name',)

    name = 'Component'


class ComponentStatisticFactory(factory.DjangoModelFactory):
    class Meta:
        model = ComponentStatistic
        # django_get_or_create = ('start_date', 'end_date', 'price', 'brand', 'bike', 'component')

    bike = factory.SubFactory(BikeFactory)
    component = factory.SubFactory(ComponentFactory)

    start_date = datetime(2000, 1, 1)
    end_date = datetime(2000, 12, 31)
    price = 10.00
    brand = 'unknown'


class DataFactory(factory.DjangoModelFactory):
    class Meta:
        model = Data

    bike = factory.SubFactory(BikeFactory)

    date = datetime(2000, 1, 1)

    @factory.sequence
    def distance(n):
        return 10 * n

    @factory.sequence
    def time(n):
        return timedelta(seconds=(1000 * n))

    @factory.sequence
    def ascent(n):
        return 100 * n

    @factory.sequence
    def max_speed(n):
        return 15 * n

    @factory.sequence
    def cadence(n):
        return 85 + n

    @factory.sequence
    def heart_rate(n):
        return 140 + n

    @factory.sequence
    def temperature(n):
        return 10 * n


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = 'bob'
    password = factory.PostGenerationMethodCall('set_password', '123')
    email = 'bob@d.lt'
