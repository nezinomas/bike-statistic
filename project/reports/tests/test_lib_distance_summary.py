from datetime import date

import pytest

from ..library.distance_summary import DistanceSummary as T


@pytest.fixture(name="years")
def fixture_years():
    return [2000, 2001]


@pytest.fixture(name="bikes")
def fixture_bikes():
    return ['B1', 'B2']


@pytest.fixture(name="data")
def fixture_data():
    return [
        {'date': date(2000, 1, 1), 'bike': 'B1', 'distance': 10.0},
        {'date': date(2000, 1, 1), 'bike': 'B2', 'distance': 20.0},
        {'date': date(2001, 1, 1), 'bike': 'B2', 'distance': 35.0},
    ]


def test_table(years, bikes, data):
    expect = [
        {'year': 2000, 'B1': 10.0, 'B2': 20.0},
        {'year': 2001, 'B1': 0.0, 'B2': 35.0},
    ]
    actual = T(years, bikes, data).table

    assert actual == expect


def test_table_total_column(years, bikes, data):
    data.extend([
        {'date': date(2002, 1, 1), 'bike': 'B3', 'distance': 35.0},
    ])
    expect = [
        {'year': 2000, 'total': 30.0},
        {'year': 2001, 'total': 35.0},
        {'year': 2002, 'total': 35.0},
    ]
    actual = T(years, bikes, data).total_column

    assert actual == expect


def test_table_total_row(years, bikes, data):
    expect = {'B1': 10.0, 'B2': 55.0}
    actual = T(years, bikes, data).total_row

    assert actual == expect


def test_chart_data(years, bikes, data):
    expect = [
        {'name': 'B1', 'data': [10.0, 0.0]},
        {'name': 'B2', 'data': [20.0, 35.0]},
    ]

    actual = T(years, bikes, data).chart_data

    assert actual == expect
