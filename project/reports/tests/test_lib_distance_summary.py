from datetime import date

import pytest

from ..library.distance_summary import DistanceSummary as T


@pytest.fixture()
def _years():
    d = [2000, 2001]
    return d


@pytest.fixture()
def _bikes():
    return ['B1', 'B2']


@pytest.fixture()
def _data():
    return [
        {'date': date(2000, 1, 1), 'bike': 'B1', 'distance': 10.0},
        {'date': date(2000, 1, 1), 'bike': 'B2', 'distance': 20.0},
        {'date': date(2001, 1, 1), 'bike': 'B2', 'distance': 35.0},
    ]


def test_table(_years, _bikes, _data):
    expect = [
        {'year': 2000, 'B1': 10.0, 'B2': 20.0},
        {'year': 2001, 'B1': 0.0, 'B2': 35.0},
    ]
    actual = T(_years, _bikes, _data).table

    assert actual == expect


def test_table_years(_bikes, _data):
    expect = [
        {'year': 2000, 'B1': 10.0, 'B2': 20.0},
        {'year': 2001, 'B1': 0.0, 'B2': 35.0},
        {'year': 3000, 'B1': 0.0, 'B2': 0.0},
    ]
    actual = T([3000], _bikes, _data).table

    assert actual == expect


def test_table_total_column(_years, _bikes, _data):
    expect = [
        {'year': 2000, 'total': 30.0},
        {'year': 2001, 'total': 35.0},
    ]
    actual = T(_years, _bikes, _data).total_column

    assert actual == expect


def test_table_total_row(_years, _bikes, _data):
    expect = {'B1': 10.0, 'B2': 55.0}
    actual = T(_years, _bikes, _data).total_row

    assert actual == expect


def test_chart_data(_years, _bikes, _data):
    expect = [
        {'name': 'B1', 'data': [10.0, 0.0]},
        {'name': 'B2', 'data': [20.0, 35.0]},
    ]

    actual = T(_years, _bikes, _data).chart_data

    assert actual == expect
