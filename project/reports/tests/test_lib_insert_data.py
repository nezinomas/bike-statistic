from datetime import datetime, timedelta

import pytest

from ...core.factories import BikeFactory, DataFactory, UserFactory
from .. import models
from ..endomondo import Workout
from ..library.insert_data import get_temperature, insert_data

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def mock_workout(monkeypatch):
    mock_func = 'project.reports.library.insert_data.__workouts'
    return_val = [Workout(
        {
            'ascent': 9,
            'descent': 9,
            'distance': 10.12345,
            'duration': 15,
            'sport': 2,
            'start_time': '2000-01-01 14:48:05 UTC'
        }
    )]
    monkeypatch.setattr(mock_func, lambda maxResults: return_val)


@pytest.fixture()
def mock_get_page(monkeypatch):
    mock_func = 'project.reports.library.insert_data._get_page_content'
    string = (
        '<div class="now__weather"><span class="unit unit_temperature_c">'
        '<span class="nowvalue__text_l">'
        '<span class="nowvalue__sign">+</span>22,'
        '<span class="nowvalue__text_m">5</span>'
        '</span></span></div>'
    )
    monkeypatch.setattr(mock_func, lambda x: string)


@pytest.fixture()
def mock_get_page_exception(monkeypatch):
    mock_func = 'project.reports.library.insert_data._get_page_content'
    monkeypatch.setattr(mock_func, lambda x: Exception())


def test_get_temperature(mock_get_page):
    actual = get_temperature()

    assert 22.5 == actual


@pytest.mark.xfail(raises=Exception)
def test_get_temperature_if_exception(mock_get_page_exception):
    get_temperature()


def test_insert_data_exists(mock_get_page):
    DataFactory(
        date=datetime(2000, 1, 1).date(),
        distance=10.12,
        time=timedelta(seconds=15)
    )
    insert_data()

    actual = models.Data.objects.all()

    assert 1 == actual.count()


def test_insert_data_not_exists_1(mock_get_page):
    DataFactory(
        date=datetime(1999, 1, 1).date(),
        distance=10.10,
        time=timedelta(seconds=15)
    )

    insert_data()

    data = models.Data.objects.order_by('-pk')

    assert 2 == data.count()


def test_insert_data_not_exists_2(mock_get_page):
    DataFactory(
        date=datetime(2000, 1, 1).date(),
        distance=9.12345678,
        time=timedelta(seconds=15)
    )

    insert_data()

    data = models.Data.objects.order_by('-pk')

    assert 2 == data.count()


def test_insert_data_not_exists_3(mock_get_page_exception):
    DataFactory(
        date=datetime(2000, 1, 1).date(),
        distance=9.12345678,
        time=timedelta(seconds=15)
    )

    insert_data()

    data = [*models.Data.objects.order_by('-pk')]

    assert 2 == len(data)
    assert data[0].temperature is None


def test_insert_data_must_be_rounded(mock_get_page):
    BikeFactory()

    insert_data()

    data = models.Data.objects.order_by('-pk')
    inserted_row = data[0]

    assert 1 == data.count()
    assert 10.12 == inserted_row.distance
