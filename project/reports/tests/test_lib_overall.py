from datetime import datetime, timedelta

import pandas as pd
import pandas.api.types as ptypes
import pytest

from ...core.factories import BikeFactory, DataFactory
from ..library.overall import Overall

pytestmark = pytest.mark.django_db


def set_date(year, month, day):
    return datetime(year, month, day).date()


@pytest.fixture()
def df():
    data = {
        'date': [set_date(2017, 1, 1), set_date(2018, 1, 1), set_date(2017, 1, 1)],
        'distance': [10.0, 100.0, 200.0],
        'time': [timedelta(seconds=15), timedelta(seconds=115), timedelta(seconds=1115)],
        'bike__date': [set_date(1999, 1, 1), set_date(1999, 1, 1), set_date(2000, 1, 1)],
        'bike_short_name': ['bike1', 'bike1', 'bike2']
    }
    return pd.DataFrame(data)


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
    obj = Overall()

    expected = [2017, 2018]

    assert expected == obj.create_categories()


def test_create_series(db):
    obj = Overall().create_series()

    assert 2 == len(obj)

    # bike1
    assert 'bike1' == obj[0]['name']
    assert [10.0, 100.0] == obj[0]['data']

    # bike2
    assert 'bike2' == obj[1]['name']
    assert [200.0, 0.0] == obj[1]['data']
