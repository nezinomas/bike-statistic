from datetime import date, datetime, timezone
from decimal import Decimal

import pytest
import time_machine

from ..lib.component_wear import ComponentWear

pytestmark = pytest.mark.django_db


@pytest.fixture(name="data")
def fixture_data():
    return [
        {
            "date": datetime(1999, 1, 1, 0, 0, 1, tzinfo=timezone.utc),
            "distance": Decimal("10.5"),
        },
        {
            "date": datetime(1999, 1, 31, 0, 0, 1, tzinfo=timezone.utc),
            "distance": Decimal("11.5"),
        },
        {
            "date": datetime(2000, 1, 31, 0, 0, 1, tzinfo=timezone.utc),
            "distance": Decimal("12.5"),
        },
    ]


@pytest.fixture(name="stats")
def fixture_stats():
    return [
        {"start_date": date(1999, 1, 1), "end_date": date(1999, 1, 31), "pk": 1},
        {"start_date": date(2000, 1, 1), "end_date": None, "pk": 2},
    ]


def test_total_bike_distance(stats, data):
    actual = ComponentWear(stats, data).bike_km

    assert actual == 34.5


def test_total_bike_distance_no_stats_no_data():
    actual = ComponentWear([], []).bike_km

    assert not actual


def test_component_distance(stats, data):
    expect = {"1": 22.0, "2": 12.5}
    actual = ComponentWear(stats, data).component_km

    assert expect == actual


@time_machine.travel("1999-2-5 5:6:7")
def test_component_distance_with_datetimes():
    data = [
        {"date": datetime(1999, 2, 2, 3, 2, 1), "distance": Decimal("1")},
        {"date": datetime(1999, 2, 3, 3, 2, 1), "distance": Decimal("2")},
        {"date": datetime(1999, 2, 4, 3, 2, 1), "distance": Decimal("4")},
        {"date": datetime(1999, 2, 5, 3, 2, 1), "distance": Decimal("5")},
    ]

    stats = [
        {"start_date": date(1999, 2, 1), "end_date": date(1999, 2, 3), "pk": 1},
        {"start_date": date(1999, 2, 4), "end_date": None, "pk": 2},
    ]

    expect = {"1": 3, "2": 9}
    actual = ComponentWear(stats, data).component_km

    assert expect == actual


def test_component_distance_no_data(stats):
    expect = {"1": 0, "2": 0}
    actual = ComponentWear(stats, []).component_km

    assert expect == actual


def test_component_distance_no_data_stats_one_record_and_no_end_data():
    stats = [{"start_date": date(2000, 1, 1), "end_date": None, "pk": 2}]
    expect = {"2": 0}
    actual = ComponentWear(stats, []).component_km

    assert expect == actual


def test_component_distance_no_components():
    expect = []
    actual = ComponentWear([], []).component_km

    assert expect == actual


def test_component_stats(stats, data):
    actual = ComponentWear(stats, data).component_stats

    assert actual["avg"] == 17.25
    assert actual["median"] == 17.25


def test_component_stats_no_data(stats):
    actual = ComponentWear(stats, []).component_stats

    assert actual["avg"] == 0
    assert actual["median"] == 0


def test_component_stats_no_components():
    actual = ComponentWear([], []).component_stats

    assert actual["avg"] == 0
    assert actual["median"] == 0
