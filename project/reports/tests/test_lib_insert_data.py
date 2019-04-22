from datetime import datetime, timedelta

import pytest
from mock import patch

from .. import models
from ...core.factories import BikeFactory, DataFactory, UserFactory
from ..endomondo import Workout
from ..library.insert_data import insert_data

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def login(client):
    UserFactory()
    client.login(username='bob', password='123')


@pytest.fixture(scope='module', autouse=True)
def mock_workout():
    mock_func = 'project.reports.library.insert_data.__workouts'
    with patch(mock_func) as mocked:
        mocked.return_value = [Workout(
            {
                'ascent': 9,
                'descent': 9,
                'distance': 10.12345,
                'duration': 15,
                'sport': 2,
                'start_time': '2000-01-01 14:48:05 UTC'
            })]
        yield


@pytest.fixture(scope='session', autouse=True)
def mock_get_temperature():
    mock_func = 'project.reports.library.insert_data.get_temperature'
    with patch(mock_func) as mocked:
        mocked.return_value = 1.5
        yield


def test_insert_data_exists():
    DataFactory(
        date=datetime(2000, 1, 1).date(),
        distance=10.12,
        time=timedelta(seconds=15)
    )
    insert_data()

    actual = models.Data.objects.all()

    assert 1 == actual.count()


def test_insert_data_not_exists_1():
    DataFactory(
        date=datetime(1999, 1, 1).date(),
        distance=10.10,
        time=timedelta(seconds=15)
    )

    insert_data()

    data = models.Data.objects.order_by('-pk')

    assert 2 == data.count()


def test_insert_data_not_exists_2():
    DataFactory(
        date=datetime(2000, 1, 1).date(),
        distance=9.12345678,
        time=timedelta(seconds=15)
    )

    insert_data()

    data = models.Data.objects.order_by('-pk')

    assert 2 == data.count()


def test_insert_data_must_be_rounded():
    BikeFactory()

    insert_data()

    data = models.Data.objects.order_by('-pk')
    inserted_row = data[0]

    assert 1 == data.count()
    assert 10.12 == inserted_row.distance
