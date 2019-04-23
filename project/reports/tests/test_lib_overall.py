from datetime import datetime, timedelta

import pytest
from django.test import TestCase

from ...core.factories import BikeFactory, DataFactory
from ..library.overall import Overall
from ..models import Data
from ...bikes import models as M

pytestmark = pytest.mark.django_db


@pytest.fixture(scope='module', autouse=True)
def data(django_db_blocker):
    with django_db_blocker.unblock():
        bike1 = BikeFactory(
            short_name='bike1',
            full_name='bike1',
            date=datetime(1999, 1, 1).date()
        )
        bike2 = BikeFactory(
            short_name='bike2',
            full_name='bike2',
            date=datetime(2000, 1, 1).date()
        )
        DataFactory(bike=bike1, date=datetime(2017, 1, 1).date(),
                    distance=10.0, time=timedelta(seconds=15))
        DataFactory(bike=bike1, date=datetime(2018, 1, 1).date(),
                    distance=100.0, time=timedelta(seconds=15))
        DataFactory(bike=bike2, date=datetime(2017, 1, 1).date(),
                    distance=200.0, time=timedelta(seconds=15))


def test_create_categories(db):
    obj = Overall(Data)

    expected = [2017, 2018]

    assert expected == obj.create_categories()


def test_create_series(db):
    obj = Overall(Data).create_series()

    assert 2 == len(obj)

    # bike1
    assert 'bike1' == obj[0]['name']
    assert [10.0, 100.0] == obj[0]['data']

    # bike2
    assert 'bike2' == obj[1]['name']
    assert [200.0, 0.0] == obj[1]['data']
