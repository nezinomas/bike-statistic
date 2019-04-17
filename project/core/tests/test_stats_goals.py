from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import pandas.api.types as ptypes
import pytest
from django.http import Http404

from ...goals.factories import GoalFactory
from ...reports.factories import BikeFactory, DataFactory
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

    def test_get_goals_raise_execption_01(self):
        with pytest.raises(Http404):
            actual = T(3000)._StatsGoals__get_goals


@pytest.mark.django_db
class TestGetDf():
    def test_df_empty(self):
        actual = T()._StatsGoals__df

        assert 0 == len(actual)

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
