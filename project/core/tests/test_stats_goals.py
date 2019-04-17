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


def test_get_goals_all():
    actual = T()._StatsGoals__goals

    assert 2 == len(actual)


def test_get_goals_one():
    actual = T(2000)._StatsGoals__goals

    assert 1 == len(actual)


def test_get_goals_raise_execption_01():
    with pytest.raises(Http404):
        actual = T(3000)._StatsGoals__get_goals


def test_df_empty():
    actual = T()._StatsGoals__df

    assert 0 == len(actual)
