from datetime import datetime, timedelta

import pytest

from ...bikes.factories import BikeFactory
from ...reports.factories import DataFactory
from .. import models
from ..endomondo import Workout
from ..library.insert_data import get_temperature, insert_data

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def _workout(monkeypatch):
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
def _get_page(monkeypatch):
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
def _get_page_exception(monkeypatch):
    mock_func = 'project.reports.library.insert_data._get_page_content'
    monkeypatch.setattr(mock_func, lambda x: Exception())


def test_get_temperature(_get_page):
    actual = get_temperature()

    assert actual == 22.5


@pytest.mark.xfail(raises=Exception)
def test_get_temperature_if_exception(_get_page_exception):
    get_temperature()


def test_insert_data_exists(_get_page):
    DataFactory(
        date=datetime(2000, 1, 1).date(),
        distance=10.12,
        time=timedelta(seconds=15)
    )
    insert_data()

    actual = models.Data.objects.all()

    assert actual.count() == 1


def test_insert_data_not_exists_1(_get_page, get_user):
    DataFactory(
        date=datetime(1999, 1, 1).date(),
        distance=10.10,
        time=timedelta(seconds=15)
    )

    insert_data()

    data = models.Data.objects.order_by('-pk')

    assert data.count() == 2

    for row in data:
        assert row.user.username == 'bob'


def test_insert_data_not_exists_2(_get_page, get_user):
    DataFactory(
        date=datetime(2000, 1, 1).date(),
        distance=9.12345678,
        time=timedelta(seconds=15)
    )

    insert_data()

    data = models.Data.objects.order_by('-pk')

    assert data.count() == 2

    for row in data:
        assert row.user.username == 'bob'

def test_insert_data_not_exists_3(_get_page_exception, get_user):
    DataFactory(
        date=datetime(2000, 1, 1).date(),
        distance=9.12345678,
        time=timedelta(seconds=15)
    )

    insert_data()

    data = [*models.Data.objects.order_by('-pk')]

    assert len(data) == 2
    assert data[0].temperature is None

    for row in data:
        assert row.user.username == 'bob'


def test_insert_data_must_be_rounded(_get_page, get_user):
    BikeFactory()

    insert_data()

    data = models.Data.objects.order_by('-pk')
    inserted_row = data[0]

    assert data.count() == 1
    assert inserted_row.distance == 10.12
