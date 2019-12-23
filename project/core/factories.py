from datetime import datetime, timedelta

import factory

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

    @factory.sequence
    def date(n):
        return datetime(2000, 1, 1)

    @factory.sequence
    def distance(n):
        return 10 * (n + 1)

    @factory.sequence
    def time(n):
        return timedelta(seconds=(1000 * (n + 1)))

    @factory.sequence
    def ascent(n):
        return 100 * (n + 1)

    @factory.sequence
    def max_speed(n):
        return 15 * (n + 1)

    @factory.sequence
    def cadence(n):
        return 85 + (n + 1)

    @factory.sequence
    def heart_rate(n):
        return 140 + (n + 1)

    @factory.sequence
    def temperature(n):
        return 10 * (n + 1)
