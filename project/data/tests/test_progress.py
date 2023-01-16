from datetime import date, datetime, timedelta

import pytest

from ...users.factories import UserFactory
from ..factories import DataFactory
from ..library.progress import Progress


pytestmark = pytest.mark.django_db


@pytest.fixture()
def _data(get_user):
    DataFactory(
        date=date(2000, 1, 1),
        distance=10.0,
        time=timedelta(seconds=1000),
        temperature=10,
        ascent=100
    )
    DataFactory(
        date=date(2000, 1, 31),
        distance=20.0,
        time=timedelta(seconds=2000),
        temperature=20,
        ascent=200
    )
    DataFactory(
        date=date(2001, 1, 31),
        distance=200.0,
        time=timedelta(seconds=20000),
        temperature=200,
        ascent=2000
    )


# ---------------------------------------------------------------------------------------
#                                                                               extremums
# ---------------------------------------------------------------------------------------
def test_extremums_no_data(get_user):
    actual = Progress(2000).extremums()

    assert not actual


def test_extremums_different_user(get_user):
    DataFactory(user=UserFactory(username='xxx'))

    actual = Progress(2000).extremums()

    assert not actual


def test_extremums_distance_one_season(get_user):
    DataFactory()
    DataFactory(date=date(2000, 1, 10), distance=25.0)
    DataFactory(date=date(3000, 1, 10), distance=35.0)

    actual = Progress(2000).extremums()

    actual = actual.get(2000)

    assert actual['distance_max_value'] == 25.0
    assert actual['distance_max_date'] == date(2000, 1, 10)

    assert actual['distance_min_value'] == 10.0
    assert actual['distance_min_date'] == date(2000, 1, 1)


def test_data_extremums_distance_all_seasons(get_user):
    DataFactory()
    DataFactory(date=date(2000, 1, 10), distance=25.0)
    DataFactory(date=date(2010, 1, 10), distance=35.0)

    actual = Progress().extremums()

    # year 3000
    assert actual[2010]['distance_max_date'] == date(2010, 1, 10)
    assert actual[2010]['distance_max_value'] == 35.0

    assert actual[2010]['distance_min_date'] == date(2010, 1, 10)
    assert actual[2010]['distance_min_value'] == 35.0

    # year 2000
    assert actual[2000]['distance_max_date'] == date(2000, 1, 10)
    assert actual[2000]['distance_max_value'] == 25.0

    assert actual[2000]['distance_min_date'] == date(2000, 1, 1)
    assert actual[2000]['distance_min_value'] == 10.0


def test_data_extremums_temperature_one_season(get_user):
    DataFactory(temperature=-1)
    DataFactory(date=date(2000, 1, 10), temperature=25.0)
    DataFactory(date=date(2010, 1, 10), temperature=35.0)


    actual = Progress(2000).extremums()
    actual = actual[2000]

    assert actual['temp_max_date'] == date(2000, 1, 10)
    assert actual['temp_max_value'] == 25.0

    assert actual['temp_min_date'] == date(2000, 1, 1)
    assert actual['temp_min_value'] == -1.0


def test_data_extremums_ascent_one_season(get_user):
    DataFactory()
    DataFactory(date=date(2000, 1, 10), ascent=250)
    DataFactory(date=date(2010, 1, 10), ascent=350)

    actual = Progress(2000).extremums()
    actual = actual[2000]

    assert actual['ascent_max_date'] == date(2000, 1, 10)
    assert actual['ascent_max_value'] == 250


def test_data_extremums_speed_one_season(get_user):
    DataFactory()
    DataFactory(date=date(2000, 1, 10), distance=25.0)
    DataFactory(date=date(3000, 1, 10), distance=35.0)

    actual = Progress(2000).extremums()
    actual = actual[2000]

    assert actual['speed_max_date'] == date(2000, 1, 10)
    assert actual['speed_max_value'] == 90.0


# ---------------------------------------------------------------------------------------
#                                                                               distances
# ---------------------------------------------------------------------------------------
def test_distances_one_season(get_user):
    DataFactory()
    DataFactory(date=date(2000, 1, 10), distance=25.0)
    DataFactory(date=date(3000, 1, 10), distance=35.0)

    actual = Progress(2000).distances()

    assert len(actual) == 1
    assert actual[2000]['distance'] == 35.0



def test_data_distances_all_seasons(get_user):
    DataFactory()
    DataFactory(date=date(2000, 1, 10), distance=30.0)
    DataFactory(date=date(2010, 1, 10), distance=35.0)

    actual = Progress().distances()

    assert len(actual) == 2
    assert actual[2010]['distance'] == 35.0
    assert actual[2000]['distance'] == 40.0


# ---------------------------------------------------------------------------------------
#                                                                             month stats
# ---------------------------------------------------------------------------------------
def test_month_stats(_data):
    actual = Progress(2000).month_stats()

    assert len(actual) == 1

    actual = actual['2000-01']

    assert actual['distance'] == 30.0
    assert actual['ascent'] == 300
    assert round(actual['seconds'], 1) == 3000
    assert round(actual['speed'], 1) == 36.0
    assert actual['monthlen'] == 31
    assert round(actual['distance_per_day'], 4) == 0.9677


# ---------------------------------------------------------------------------------------
#                                                                         season progress
# ---------------------------------------------------------------------------------------
def test_season_progress_keys(_data):
    actual = Progress(2000).season_progress(goal=1000)

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


def test_season_progress_no_year(_data):
    actual = Progress().season_progress()

    assert actual == {}


def test_season_progress_sorting(_data):
    actual = Progress(2000).season_progress(goal=1000)

    assert datetime(2000, 1, 31) == actual[0]['date']
    assert datetime(2000, 1, 1) == actual[1]['date']


def test_season_progress_distance_cumulative_sum(_data):
    actual = Progress(2000).season_progress(goal=1000)

    assert actual[0]['season_distance'] == 30.0
    assert actual[1]['season_distance'] == 10.0


def test_season_progress_seconds_cumulative_sum(_data):
    actual = Progress(2000).season_progress(goal=1000)

    assert round(actual[0]['season_seconds'], 1) == 3000
    assert round(actual[1]['season_seconds'], 1) == 1000


def test_season_progress_season_speed(_data):
    actual = Progress(2000).season_progress(goal=1000)

    assert round(actual[0]['season_speed'], 1) == 36.0
    assert round(actual[1]['season_speed'], 1) == 36.0


def test_season_progress_goal_percents(_data):
    actual = Progress(2000).season_progress(goal=1000)

    assert round(actual[0]['goal_percent'], 1) == 35.4
    assert round(actual[1]['goal_percent'], 1) == 366.0


def test_season_progress_day_goal(_data):
    actual = Progress(2000).season_progress(goal=1000)

    assert round(actual[0]['goal_day'], 3) == 84.699
    assert round(actual[1]['goal_day'], 3) == 2.732


def test_season_progress_day_goal_empty(_data):
    actual = Progress(2000).season_progress()
    assert actual[0]['goal_day'] == 0.0
    assert actual[1]['goal_day'] == 0.0


def test_season_progress_km_delta(_data):
    actual = Progress(2000).season_progress(goal=1000)

    assert round(actual[0]['goal_delta'], 3) == -54.699
    assert round(actual[1]['goal_delta'], 3) == 7.268


def test_season_progress_per_day_season(_data):
    actual = Progress(2000).season_progress(goal=1000)

    assert round(actual[0]['season_per_day'], 3) == 0.968
    assert round(actual[1]['season_per_day'], 3) == 10.0


def test_season_progress_ascent_cumulative_sum(_data):
    actual = Progress(2000).season_progress(goal=1000)

    assert actual[0]['season_ascent'] == 300
    assert actual[1]['season_ascent'] == 100


def test_season_progress_workout_speed(_data):
    actual = Progress(2000).season_progress(goal=1000)

    assert round(actual[0]['speed'], 1) == 36.0
    assert round(actual[1]['speed'], 1) == 36.0


def test_season_progress_day_num(_data):
    actual = Progress(2000).season_progress(goal=1000)

    assert actual[0]['day_nr'] == 31
    assert actual[1]['day_nr'] == 1
