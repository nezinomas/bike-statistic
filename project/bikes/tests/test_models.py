from datetime import date

import pytest

from ...users.factories import UserFactory
from ..factories import BikeFactory, BikeInfoFactory
from ..models import Bike, BikeInfo

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
    _user = UserFactory(username='XXX')
    _date = date(1, 1, 1)

    Bike.objects.create(user=_user, short_name='X', date=_date)
    Bike.objects.create(user=_user, short_name='X', date=_date)


def test_bike_short_name_unique_for_two_users(get_user):
    BikeFactory()
    BikeFactory(user=UserFactory(username='XXX'))


def test_bike_related_qs_count(get_user, django_assert_max_num_queries):
    BikeFactory(short_name='C1')
    BikeFactory(short_name='C2')

    assert Bike.objects.all().count() == 2

    with django_assert_max_num_queries(1):
        list(q.short_name for q in Bike.objects.related())


# ----------------------------------------------------------------------------
#                                                                    Bike Info
# ----------------------------------------------------------------------------
def test_bike_info_str():
    obj = BikeInfoFactory.build()

    assert str(obj) == 'Short Name: Component'


def test_bike_info_related_different_users(get_user):
    u = UserFactory(username='tom')

    b1 = BikeFactory(short_name='B1')  # user bob
    b2 = BikeFactory(short_name='B2', user=u)  # user tom

    BikeInfoFactory(component='N1', bike=b1)
    BikeInfoFactory(component='N2', bike=b2)

    actual = BikeInfo.objects.related()

    # expense names for user bob
    assert len(actual) == 1
    assert actual[0].component == 'N1'


def test_bike_info_related_qs_count(get_user, django_assert_max_num_queries):
    BikeInfoFactory(component='C1')
    BikeInfoFactory(component='C2')

    assert BikeInfo.objects.all().count() == 2

    with django_assert_max_num_queries(1):
        list(q.bike.short_name for q in BikeInfo.objects.related())


def test_bike_info_items(get_user):
    BikeInfoFactory()

    assert BikeInfo.objects.items().count() == 1
