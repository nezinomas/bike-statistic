from datetime import datetime, timedelta

import pandas as pd
import pandas.api.types as ptypes
import pytest

from ..library.overall import Overall

pytestmark = pytest.mark.django_db


def set_date(year, month, day):
    return datetime(year, month, day).date()


def df():
    data = {
        'date': [set_date(2017, 1, 1), set_date(2018, 1, 1), set_date(2017, 1, 1)],
        'distance': [10.0, 100.0, 200.0],
        'time': [timedelta(seconds=15), timedelta(seconds=115), timedelta(seconds=1115)],
        'bike__date': [set_date(1999, 1, 1), set_date(1999, 1, 1), set_date(2000, 1, 1)],
        'bike__short_name': ['bike1', 'bike1', 'bike2']
    }
    return pd.DataFrame(data)


@pytest.fixture(autouse=True)
def mock_Overall__create_query(monkeypatch, request):
    if 'noautofixt' in request.keywords:
        return

    monkeypatch.setattr(Overall, '_Overall__create_query', lambda x: True)


@pytest.fixture(autouse=True)
def mock_read_frame(monkeypatch):
    mock_target = 'project.reports.library.overall.read_frame'
    monkeypatch.setattr(mock_target, lambda x: df())


def test_df_date_type():
    actual = Overall().df

    assert ptypes.is_int64_dtype(actual['date'])


def test_create_categories():
    actual = Overall().years
    expected = [2017, 2018]

    assert expected == actual


def test_distances():
    actual = Overall().distances
    expected = [[10.0, 100.0], [200.0, 0.0]]

    assert expected == actual


def test_bikes():
    actual = Overall().bikes
    expected = ['bike1', 'bike2']

    assert expected == actual


@pytest.mark.django_db
@pytest.mark.noautofixt
def test_no_data():
    with pytest.raises(Exception) as excinfo:
        Overall()

    assert str(excinfo.value) == 'No data in db.'
