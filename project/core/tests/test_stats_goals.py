from datetime import datetime, timedelta

import pandas as pd
import pandas.api.types as ptypes
import pytest
from django.http import Http404

from ...goals.factories import GoalFactory
from ...core.factories import DataFactory
from ..lib.stats_goals import StatsGoals as T

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def create_goal():
    GoalFactory(year=2000, goal=1000)
    GoalFactory(year=2001, goal=2000)


@pytest.mark.django_db
class TestGetGoals():
    def test_get_goals_all(self):
        actual = T()._StatsGoals__goals

        assert 2 == len(actual)

    def test_get_goals_one(self):
        actual = T(2000)._StatsGoals__goals

        assert 1 == len(actual)

    @pytest.mark.xfail(raises=Http404)
    def test_get_goals_raise_execption_01(self):
        T(3000)._StatsGoals__get_goals


@pytest.mark.django_db
class TestGetDf():
    def test_df_empty(self):
        actual = T()._StatsGoals__df

        assert 0 == len(actual)

    def test_table_df_empty(self):
        actual = T().year_progress()

        assert actual is None

    def test_stats_df_empty(self):
        actual = T().year_stats()

        assert actual is None

    def test_df_not_empty(self):
        DataFactory(
            date=datetime(2017, 1, 1).date(),
            distance=10.0,
            time=timedelta(seconds=15)
        )
        actual = T()._StatsGoals__df

        assert 1 == len(actual)

        assert ptypes.is_datetime64_dtype(actual['date'])
        assert ptypes.is_float_dtype(actual['distance'])
        assert ptypes.is_integer_dtype(actual['ascent'])
        assert ptypes.is_timedelta64_dtype(actual['time'])

        assert round(actual.loc[0, 'sec_workout'], 1) == 15.0


class TestMarginalValues():
    @pytest.fixture(scope='class')
    def df(self, request):
        return pd.DataFrame(
            [
                [datetime(2000, 1, 1), 10],
                [datetime(2000, 1, 15), 15],
                [datetime(2000, 1, 20), 20]
            ],
            columns=['date', 'col']
        )

    def test_marginal_values_df_empty(self):
        actual = T()._StatsGoals__marginal_values(pd.DataFrame(), 'col', 'max')
        assert not actual

    def test_marginal_values_col_not_exists(self):
        actual = T()._StatsGoals__marginal_values(pd.DataFrame(), 'col1', 'max')
        assert not actual

    def test_marginal_values_function_not_exists(self):
        actual = T()._StatsGoals__marginal_values(pd.DataFrame(), 'col', 'maxx')
        assert not actual

    def test_marginal_values_max(self, df):
        actual = T()._StatsGoals__marginal_values(df, 'col', 'max')

        assert 20 == actual['max_col_value']
        assert datetime(2000, 1, 20) == actual['max_col_date']

    def test_marginal_values_min(self, df):
        actual = T()._StatsGoals__marginal_values(df, 'col', 'min')

        assert 10 == actual['min_col_value']
        assert datetime(2000, 1, 1) == actual['min_col_date']


@pytest.mark.django_db
class TestStatsGoals():
    @pytest.fixture(autouse=True)
    def insert_data(self):
        DataFactory(
            date=datetime(2000, 1, 1).date(),
            distance=10.0,
            time=timedelta(seconds=1000),
            temperature=10,
            ascent=100
        )
        DataFactory(
            date=datetime(2000, 1, 31).date(),
            distance=20.0,
            time=timedelta(seconds=2000),
            temperature=20,
            ascent=200
        )
        DataFactory(
            date=datetime(2001, 1, 31).date(),
            distance=200.0,
            time=timedelta(seconds=20000),
            temperature=200,
            ascent=2000
        )

    def test_year_stats(self):
        actual = T(2000).year_stats()

        assert 10 == len(actual)

        assert 10 == actual['min_temperature_value']
        assert datetime(2000, 1, 1) == actual['min_temperature_date']

        assert 20 == actual['max_temperature_value']
        assert datetime(2000, 1, 31) == actual['max_temperature_date']

        assert 200 == actual['max_ascent_value']
        assert datetime(2000, 1, 31) == actual['max_ascent_date']

        assert 20 == actual['max_distance_value']
        assert datetime(2000, 1, 31) == actual['max_distance_date']

        assert 36.00 == round(actual['max_speed_value'], 2)
        assert datetime(2000, 1, 31) == actual['max_speed_date']

    def test_all_goals_stats(self):
        actual = T().all_goals_stats()

        assert 2 == len(actual)

        assert 2001 == actual[0]['year']
        assert 200.0 == actual[0]['distance']

        assert 2000 == actual[1]['year']
        assert 30.0 == actual[1]['distance']

    def test_month_stats(self):
        actual = T(2000).month_stats()

        assert 1 == len(actual)

        actual = actual['2000-01']

        assert 30.0 == actual['distance']
        assert 300 == actual['ascent']
        assert 3000.0 == round(actual['sec_workout'], 1)
        assert 36.0 == round(actual['speed_month'], 1)
        assert 31 == actual['days_in_month']
        assert 0.9677 == round(actual['per_day_month'], 4)

    def test_year_progres_keys(self):
        actual = T(2000).year_progress()

        assert 'id' in actual[0]
        assert 'date' in actual[0]
        assert 'bike' in actual[0]
        assert 'distance' in actual[0]
        assert 'temperature' in actual[0]
        assert 'time' in actual[0]
        assert 'ascent' in actual[0]
        assert 'sec_workout' in actual[0]
        assert 'day_num' in actual[0]
        assert 'year_month' in actual[0]
        assert 'speed_workout' in actual[0]
        assert 'distance_season' in actual[0]
        assert 'sec_season' in actual[0]
        assert 'ascent_season' in actual[0]
        assert 'speed_season' in actual[0]
        assert 'per_day_season' in actual[0]
        assert 'day_goal' in actual[0]
        assert 'percent' in actual[0]
        assert 'km_delta' in actual[0]

    def test_year_progress_sorting(self):
        actual = T(2000).year_progress()

        assert datetime(2000, 1, 31) == actual[0]['date']
        assert datetime(2000, 1, 1) == actual[1]['date']

    def test_year_progress_distance_cumulative_sum(self):
        actual = T(2000).year_progress()

        assert 30.0 == actual[0]['distance_season']
        assert 10.0 == actual[1]['distance_season']

    def test_year_progress_seconds_cumulative_sum(self):
        actual = T(2000).year_progress()

        assert 3000.0 == round(actual[0]['sec_season'], 1)
        assert 1000.0 == round(actual[1]['sec_season'], 1)

    def test_year_progress_speed_season(self):
        actual = T(2000).year_progress()

        assert 36.0 == round(actual[0]['speed_season'], 1)
        assert 36.0 == round(actual[1]['speed_season'], 1)

    def test_year_progress_goal_percents(self):
        actual = T(2000).year_progress()

        assert 35.4 == round(actual[0]['percent'], 1)
        assert 366.0 == round(actual[1]['percent'], 1)

    def test_year_progress_day_goal(self):
        actual = T(2000).year_progress()

        assert 84.699 == round(actual[0]['day_goal'], 3)
        assert 2.732 == round(actual[1]['day_goal'], 3)

    def test_year_progress_km_delta(self):
        actual = T(2000).year_progress()

        assert -54.699 == round(actual[0]['km_delta'], 3)
        assert 7.268 == round(actual[1]['km_delta'], 3)

    def test_year_progress_per_day_season(self):
        actual = T(2000).year_progress()

        assert 0.968 == round(actual[0]['per_day_season'], 3)
        assert 10.0 == round(actual[1]['per_day_season'], 3)

    def test_year_progress_ascent_cumulative_sum(self):
        actual = T(2000).year_progress()

        assert 300 == actual[0]['ascent_season']
        assert 100 == actual[1]['ascent_season']

    def test_year_progress_workout_speed(self):
        actual = T(2000).year_progress()

        assert 36.0 == round(actual[0]['speed_workout'], 1)
        assert 36.0 == round(actual[1]['speed_workout'], 1)

    def test_year_progress_day_num(self):
        actual = T(2000).year_progress()

        assert 31 == actual[0]['day_num']
        assert 1 == actual[1]['day_num']
