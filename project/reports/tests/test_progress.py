from datetime import date, datetime, timedelta
from types import SimpleNamespace

import pytest

from ..library.progress import Progress

pytestmark = pytest.mark.django_db


@pytest.fixture(name="data")
def fixture_data():
    data = [
        {'date': date(2000, 1, 1), 'distance': 10, 'time': timedelta(seconds=1000), 'ascent': 100, 'bikes': 'Short Name', 'temp': 10},
        {'date': date(2000, 1, 2), 'distance': 20, 'time': timedelta(seconds=2000), 'ascent': 200, 'bikes': 'Short Name', 'temp': 20} ,
        {'date': date(2000, 1, 31), 'distance': 200, 'time': timedelta(seconds=20000), 'ascent': 2000, 'bikes': 'Short Name', 'temp': 200},
    ]

    return SimpleNamespace(year=2000, goal=1000, data=data)


@pytest.fixture(name="no_data")
def fixture_no_data():

    return SimpleNamespace(year=2000, goal=0, data=[])


# ---------------------------------------------------------------------------------------
#                                                                               extremums
# ---------------------------------------------------------------------------------------
def test_extremums_no_data(no_data):
    actual = Progress(no_data).extremums()

    assert not actual


def test_extremums_distance(data):
    actual = Progress(data).extremums()

    assert actual['distance_max_value'] == 200.0
    assert actual['distance_max_date'] == date(2000, 1, 31)

    assert actual['distance_min_value'] == 10.0
    assert actual['distance_min_date'] == date(2000, 1, 1)


def test_extremums_temperature(data):
    actual = Progress(data).extremums()

    assert actual['temp_max_date'] == date(2000, 1, 31)
    assert actual['temp_max_value'] == 200

    assert actual['temp_min_date'] == date(2000, 1, 1)
    assert actual['temp_min_value'] == 10.0


def test_extremums_ascent(data):
    actual = Progress(data).extremums()

    assert actual['ascent_max_date'] == date(2000, 1, 31)
    assert actual['ascent_max_value'] == 2000


def test_extremums_speed(data):
    actual = Progress(data).extremums()

    assert actual['speed_max_date'] == date(2000, 1, 1)
    assert actual['speed_max_value'] == 36.0


def test_month_stats(data):
    actual = Progress(data).month_stats()

    assert len(actual) == 1

    actual = actual['2000-01']

    assert actual['distance'] == 230.0
    assert actual['ascent'] == 2300
    assert round(actual['seconds'], 1) == 23000
    assert round(actual['speed'], 1) == 36.0
    assert actual['monthlen'] == 31
    assert round(actual['distance_per_day'], 2) == 7.42


def test_season_progress_keys(data):
    actual = Progress(data).season_progress()

    assert 'date' in actual[0]
    assert 'bikes' in actual[0]
    assert 'distance' in actual[0]
    assert 'temp' in actual[0]
    assert 'time' in actual[0]
    assert 'ascent' in actual[0]
    assert 'seconds' in actual[0]
    assert 'day_nr' in actual[0]
    assert 'year_month' in actual[0]
    assert 'speed' in actual[0]
    assert 'season_distance' in actual[0]
    assert 'season_seconds' in actual[0]
    assert 'season_ascent' in actual[0]
    assert 'season_speed' in actual[0]
    assert 'season_per_day' in actual[0]
    assert 'goal_day' in actual[0]
    assert 'goal_percent' in actual[0]
    assert 'goal_delta' in actual[0]


def test_season_progress_sorting(data):
    actual = Progress(data).season_progress()

    assert datetime(2000, 1, 31) == actual[0]['date']
    assert datetime(2000, 1, 2) == actual[1]['date']
    assert datetime(2000, 1, 1) == actual[2]['date']


def test_season_progress_distance_cumulative_sum(data):
    actual = Progress(data).season_progress()

    assert actual[0]['season_distance'] == 230.0
    assert actual[1]['season_distance'] == 30.0
    assert actual[2]['season_distance'] == 10.0


def test_season_progress_seconds_cumulative_sum(data):
    actual = Progress(data).season_progress()

    assert round(actual[0]['season_seconds'], 2) == 23000
    assert round(actual[1]['season_seconds'], 2) == 3000
    assert round(actual[2]['season_seconds'], 2) == 1000


def test_season_progress_season_speed(data):
    actual = Progress(data).season_progress()

    assert round(actual[0]['season_speed'], 2) == 36.0
    assert round(actual[1]['season_speed'], 2) == 36.0
    assert round(actual[2]['season_speed'], 2) == 36.0


def test_season_progress_goal_percents(data):
    actual = Progress(data).season_progress()

    assert round(actual[0]['goal_percent'], 2) == 271.55
    assert round(actual[1]['goal_percent'], 2) == 549.0
    assert round(actual[2]['goal_percent'], 2) == 366.0


def test_season_progress_day_goal(data):
    actual = Progress(data).season_progress()

    assert round(actual[0]['goal_day'], 2) == 84.7
    assert round(actual[1]['goal_day'], 2) == 5.46
    assert round(actual[2]['goal_day'], 2) == 2.73


def test_season_progress_day_goal_empty(data):
    data.goal = 0
    actual = Progress(data).season_progress()
    assert actual[0]['goal_day'] == 0.0
    assert actual[1]['goal_day'] == 0.0
    assert actual[2]['goal_day'] == 0.0


def test_season_progress_km_delta(data):
    actual = Progress(data).season_progress()

    assert round(actual[0]['goal_delta'], 2) == 145.3
    assert round(actual[1]['goal_delta'], 2) == 24.54
    assert round(actual[2]['goal_delta'], 2) == 7.27


def test_season_progress_per_day_season(data):
    actual = Progress(data).season_progress()

    assert round(actual[0]['season_per_day'], 2) == 7.42
    assert round(actual[1]['season_per_day'], 2) == 15.0
    assert round(actual[2]['season_per_day'], 2) == 10.0


def test_season_progress_ascent_cumulative_sum(data):
    actual = Progress(data).season_progress()

    assert actual[0]['season_ascent'] == 2300
    assert actual[1]['season_ascent'] == 300
    assert actual[2]['season_ascent'] == 100


def test_season_progress_workout_speed(data):
    actual = Progress(data).season_progress()

    assert round(actual[0]['speed'], 2) == 36.0
    assert round(actual[1]['speed'], 2) == 36.0
    assert round(actual[2]['speed'], 2) == 36.0


def test_season_progress_day_num(data):
    actual = Progress(data).season_progress()

    assert actual[0]['day_nr'] == 31
    assert actual[1]['day_nr'] == 2
    assert actual[2]['day_nr'] == 1
