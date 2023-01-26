from datetime import date
from decimal import Decimal

import pytest

from ..lib.component_wear import ComponentWear

pytestmark = pytest.mark.django_db


@pytest.fixture(name="data")
def fixture_data():
    return [
        {'date': date(1999, 1, 1), 'distance': Decimal('10.5')},
        {'date': date(1999, 1, 31), 'distance': Decimal('11.5')},
        {'date': date(2000, 1, 31), 'distance': Decimal('12.5')},
    ]

@pytest.fixture(name="stats")
def fixture_stats():
    return [
        {'start_date': date(1999, 1, 1), 'end_date': date(1999, 1, 31), 'pk': 1},
        {'start_date': date(2000, 1, 1), 'end_date': None, 'pk': 2},
    ]


def test_total_bike_distance(stats, data):
    actual = ComponentWear(stats, data).bike_km

    assert actual == 34.5


def test_total_bike_distance_no_stats_no_data():
    actual = ComponentWear([], []).bike_km

    assert not actual


def test_component_distance(stats, data):
    expect = {'1': 22.0, '2': 12.5}
    actual = ComponentWear(stats, data).component_km

    assert expect == actual


def test_component_distance_no_data(stats):
    expect = {'1': 0, '2': 0}
    actual = ComponentWear(stats, []).component_km

    assert expect == actual

def test_component_distance_no_components():
    expect = []
    actual = ComponentWear([], []).component_km

    assert expect == actual


def test_component_stats(stats, data):
    actual = ComponentWear(stats, data).component_stats

    assert actual['avg'] == 17.25
    assert actual['median'] == 17.25


def test_component_stats_no_data(stats):
    actual = ComponentWear(stats, []).component_stats

    assert actual['avg'] == 0
    assert actual['median'] == 0


def test_component_stats_no_components():
    actual = ComponentWear([], []).component_stats

    assert actual['avg'] == 0
    assert actual['median'] == 0
