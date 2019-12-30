import pytest

from ..models import Bike, BikeInfo
from ..factories import BikeFactory
from ...users.factories import UserFactory

pytestmark = pytest.mark.django_db


# ----------------------------------------------------------------------------
#                                                                         Bike
# ----------------------------------------------------------------------------
def test_bike_str():
    obj = BikeFactory.build()

    assert str(obj) == 'Short Name'


def test_bike_slug():
    obj = BikeFactory()

    assert obj.slug == 'short-name'


def test_bike_items(get_user):
    BikeFactory()

    assert Bike.objects.items().count() == 1


def test_bike_items_for_logged_user(get_user):
    BikeFactory()
    BikeFactory(user=UserFactory(username='XXX'))

    assert Bike.objects.all().count() == 2
    assert Bike.objects.items().count() == 1


@pytest.mark.xfail
def test_bike_short_name_unique_for_one_user(get_user):
    BikeFactory()
    BikeFactory()


def test_bike_short_name_unique_for_two_users(get_user):
    BikeFactory()
    BikeFactory(user=UserFactory(username='XXX'))
