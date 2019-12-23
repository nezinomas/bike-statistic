import pytest

from ..models import Bike, BikeInfo
from ..factories import BikeFactory

pytestmark = pytest.mark.django_db


def test_bike_str():
    obj = BikeFactory.build()

    assert str(obj) == 'Short Name'


def test_bike_slug():
    obj = BikeFactory()

    assert obj.slug == 'short-name'


def test_bike_items():
    BikeFactory()

    assert Bike.objects.items().count() == 1
