from datetime import datetime, timedelta

import pytest

from ...bikes.factories import BikeFactory
from ...reports.factories import DataFactory
from ...users.factories import UserFactory
from ..endomondo import Workout
from ..library.insert_endomondo import (get_temperature, insert_data_all_users,
                                   insert_data_current_user)
from ..models import Data

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def _api(monkeypatch):
    mock_func = 'project.reports.library.insert_endomondo._endomondo_api'
    monkeypatch.setattr(mock_func, lambda endomondo_user, endomondo_password: None)


@pytest.fixture(autouse=True)
def _workout(monkeypatch):
    mock_func = 'project.reports.library.insert_endomondo._get_workouts'
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
    monkeypatch.setattr(mock_func, lambda api, max_results: return_val)


@pytest.fixture()
def _get_page(monkeypatch):
    mock_func = 'project.reports.library.insert_endomondo._get_weather_page'
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
    mock_func = 'project.reports.library.insert_endomondo._get_weather_page'
    monkeypatch.setattr(mock_func, lambda x: Exception())


def test_get_temperature(_get_page):
    actual = get_temperature()

    assert actual == 22.5


@pytest.mark.xfail(raises=Exception)
def test_get_temperature_if_exception(_get_page_exception):
    get_temperature()


def test_insert_endomondo_exists(_get_page, get_user):
    DataFactory(
        date=datetime(2000, 1, 1).date(),
        distance=10.12,
        time=timedelta(seconds=15)
    )
    insert_data_current_user()

    actual = Data.objects.all()

    assert actual.count() == 1


def test_insert_endomondo_not_exists_1(_get_page, get_user):
    DataFactory(
        date=datetime(1999, 1, 1).date(),
        distance=10.10,
        time=timedelta(seconds=15)
    )

    insert_data_current_user()

    data = Data.objects.order_by('-pk')

    assert data.count() == 2

    for row in data:
        assert row.user.username == 'bob'


def test_insert_endomondo_not_exists_2(_get_page, get_user):
    DataFactory(
        date=datetime(2000, 1, 1).date(),
        distance=9.12345678,
        time=timedelta(seconds=15)
    )

    insert_data_current_user()

    data = Data.objects.order_by('-pk')

    assert data.count() == 2

    for row in data:
        assert row.user.username == 'bob'

def test_insert_endomondo_not_exists_3(_get_page_exception, get_user):
    DataFactory(
        date=datetime(2000, 1, 1).date(),
        distance=9.12345678,
        time=timedelta(seconds=15)
    )

    insert_data_current_user()

    data = [*Data.objects.order_by('-pk')]

    assert len(data) == 2
    assert data[0].temperature is None

    for row in data:
        assert row.user.username == 'bob'


def test_insert_endomondo_must_be_rounded(_get_page, get_user):
    BikeFactory()

    insert_data_current_user()

    data = Data.objects.order_by('-pk')
    inserted_row = data[0]

    assert data.count() == 1
    assert inserted_row.distance == 10.12


def test_two_users(_get_page):
    u1 = UserFactory(username='U1')
    u2 = UserFactory(username='U2')

    BikeFactory(short_name='B1', user=u1)
    BikeFactory(short_name='B2', user=u2)

    insert_data_all_users()

    actual = Data.objects.all().order_by('user__username', 'bike__short_name')

    assert actual.count() == 2

    assert actual[0].user.username == 'U1'
    assert actual[1].user.username == 'U2'

    assert actual[0].bike.short_name == 'B1'
    assert actual[1].bike.short_name == 'B2'


@pytest.mark.xfail
def test_insert_all_users_no_bikes(_get_page):
    UserFactory(username='U1')
    UserFactory(username='U2')

    insert_data_all_users()


@pytest.mark.xfail
def test_insert_current_user_no_bikes(_get_page, get_user):
    insert_data_current_user()
