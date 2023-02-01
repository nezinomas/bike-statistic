from datetime import date, datetime
from zoneinfo import ZoneInfo

import pytest
from django.urls import resolve, reverse
from freezegun import freeze_time

from ...bikes.factories import BikeFactory
from ...data.factories import DataFactory
from .. import views

pytestmark = pytest.mark.django_db


@pytest.fixture(name="data")
def fixture_data():
    b1 = BikeFactory(short_name='B1', date=date(2000, 1, 1))
    b2 = BikeFactory(short_name='B2', date=date(1999, 1, 1))

    DataFactory(date=datetime(2000, 1, 1, tzinfo=ZoneInfo('Europe/Vilnius')), bike=b1, distance=10.0)
    DataFactory(date=datetime(2000, 1, 1, tzinfo=ZoneInfo('Europe/Vilnius')), bike=b2, distance=20.0)
    DataFactory(date=datetime(2001, 1, 1, tzinfo=ZoneInfo('Europe/Vilnius')), bike=b2, distance=35.0)


def test_chart_overall_func():
    view = resolve('/reports/overall/')

    assert views.ChartOverall is view.func.view_class


def test_chart_overall_200_no_data(client_logged):
    url = reverse('reports:chart_overall')
    response = client_logged.get(url)

    assert response.status_code == 200


def test_chart_overall_200(client_logged, data):
    url = reverse('reports:chart_overall')
    response = client_logged.get(url)

    assert response.status_code == 200


@freeze_time('2002-12-31')
def test_chart_overall_context_years(get_user, client_logged):
    get_user.date_joined = datetime(1998, 1, 1, tzinfo=ZoneInfo('Europe/Vilnius'))

    url = reverse('reports:chart_overall')
    response = client_logged.get(url)

    actual = response.context['year_list']

    assert actual == [1998, 1999, 2000, 2001, 2002]


def test_chart_overall_context_bikes(client_logged, data):
    url = reverse('reports:chart_overall')
    response = client_logged.get(url)

    actual = response.context['bikes']

    assert list(actual) == ['B2', 'B1']


@freeze_time('2001-01-01')
def test_chart_overall_context_data_table(client_logged, data):
    url = reverse('reports:chart_overall')
    response = client_logged.get(url)

    table = [
        {'year': 2000, 'B1': 10.0, 'B2': 20.0},
        {'year': 2001, 'B1': 0.0, 'B2': 35.0},
    ]
    total_column = [
        {'year': 2000, 'total': 30.0},
        {'year': 2001, 'total': 35.0},
    ]

    actual = response.context['table_data']

    assert actual == list(zip(table, total_column))


@freeze_time('2001-01-01')
def test_chart_overall_context_total_value(client_logged, data):
    url = reverse('reports:chart_overall')
    response = client_logged.get(url)

    actual = response.context['total']

    assert actual == 65.0


@freeze_time('2001-01-01')
def test_chart_overall_context_chart_data(client_logged, data):
    url = reverse('reports:chart_overall')
    response = client_logged.get(url)

    expect = [
        {
            'name': 'B1',
            'data': [10.0, 0.0],
            'color': 'rgba(54, 162, 235, 0.35)',
            'borderColor': 'rgba(54, 162, 235, 1)',
            'borderWidth': '0.5'
        }, {
            'name': 'B2',
            'data': [20.0, 35.0],
            'color': 'rgba(255, 99, 132, 0.35)',
            'borderColor': 'rgba(255, 99, 132, 1)',
            'borderWidth': '0.5'
        }
    ]
    actual = response.context['chart_data']

    assert actual == expect
