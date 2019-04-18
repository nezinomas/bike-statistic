from datetime import datetime

from django.contrib.auth.models import User
from factory import DjangoModelFactory, SubFactory, PostGenerationMethodCall

from ..bikes.models import Bike, Component, ComponentStatistic
from ..reports.models import Data


class BikeFactory(DjangoModelFactory):
    class Meta:
        model = Bike
        django_get_or_create = ('full_name', 'short_name', 'date')

    full_name = 'xbike'
    short_name = 'xbike'
    date = datetime(1970, 1, 1).date()


class ComponentFactory(DjangoModelFactory):
    class Meta:
        model = Component
        django_get_or_create = ('name',)

    name = 'Component'


class ComponentStatisticFactory(DjangoModelFactory):
    class Meta:
        model = ComponentStatistic
        django_get_or_create = ('start_date', 'end_date', 'price', 'brand', 'bike', 'component')

    bike = SubFactory(BikeFactory)
    component = SubFactory(ComponentFactory)

    start_date = datetime(2000, 1, 1)
    end_date = datetime(2000, 12, 31)
    price = 10.00
    brand = 'unknown'


class DataFactory(DjangoModelFactory):
    class Meta:
        model = Data

    bike = SubFactory(BikeFactory)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = 'bob'
    password = PostGenerationMethodCall('set_password', '123')
    email = 'bob@d.lt'
