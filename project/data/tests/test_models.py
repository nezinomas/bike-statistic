from datetime import date, datetime

import pytest

from ...bikes.factories import BikeFactory
from ...users.factories import UserFactory
from ..factories import DataFactory
from ..models import Data

pytestmark = pytest.mark.django_db


def test_data_str():
    obj = DataFactory.build()

    assert str(obj) == '2000-01-01 Short Name'


def test_data_related_qs_count(get_user, django_assert_max_num_queries):
    DataFactory()
    DataFactory()

    assert Data.objects.all().count() == 2

    with django_assert_max_num_queries(1):
        list(q.user.username for q in Data.objects.related())


def test_data_items(get_user):
    DataFactory()

    assert Data.objects.items().count() == 1


def test_data_items_filtered(get_user):
    DataFactory()
    DataFactory(date=date(2100, 1, 1))

    assert Data.objects.items(2000).count() == 1


def test_data_items_for_logged_user(get_user):
    DataFactory()
    DataFactory(user=UserFactory(username='XXX'))

    assert Data.objects.all().count() == 2
    assert Data.objects.items().count() == 1


def test_data_bike_summary_user_data(get_user):
    DataFactory()
    DataFactory(user=UserFactory(username='XXX'))

    assert Data.objects.all().count() == 2
    assert Data.objects.bike_summary().count() == 1


def test_data_bike_summary(get_user):
    b1 = BikeFactory(short_name='B1')

    DataFactory(bike=b1, date=datetime(2000, 1, 10))
    DataFactory(bike=b1, date=datetime(3000, 1, 10))
    DataFactory(bike=b1, date=datetime(3000, 1, 10))

    expect = [
        {'date': date(2000, 1, 1), 'bike': 'B1', 'distance': 10},
        {'date': date(3000, 1, 1), 'bike': 'B1', 'distance': 20},
    ]

    actual = list(Data.objects.bike_summary())

    assert actual == expect
