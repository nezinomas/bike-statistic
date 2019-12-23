import factory
from datetime import date
from .models import Bike, BikeInfo


class BikeFactory(factory.DjangoModelFactory):
    class Meta:
        model = Bike

    date = date(1999, 1, 1)
    full_name = 'Full Name'
    short_name = 'Short Name'
