from datetime import datetime

import pandas.api.types as ptypes
import pytest
from django.http import Http404
from freezegun import freeze_time

from ...core.factories import (ComponentFactory, ComponentStatisticFactory,
                               DataFactory)
from ..helpers.view_stats_helper import Filter as T

pytestmark = pytest.mark.django_db


@pytest.fixture(scope='module', autouse=True)
def components(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        c1 = ComponentFactory()
    yield
    with django_db_blocker.unblock():
        c1.delete()


@pytest.fixture(scope='module', autouse=True)
def components_statistic(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        c1 = ComponentStatisticFactory()
        c2 = ComponentStatisticFactory(
            start_date=datetime(2100, 1, 1).date(),
            end_date=None,
            price=100,
            brand='whatewer'
        )
    yield
    with django_db_blocker.unblock():
        c1.delete()
        c2.delete()


@pytest.fixture(scope='module', autouse=True)
def data(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        d1 = DataFactory(date=datetime(2000, 1, 1).date())
        d2 = DataFactory(date=datetime(2000, 1, 31).date())
        d3 = DataFactory(date=datetime(2100, 1, 31).date())
    yield
    with django_db_blocker.unblock():
        d1.delete()
        d2.delete()
        d3.delete()


def test_get_df():
    actual = T('bike', 1)._Filter__df

    assert 3 == len(actual)

    assert 'date' in actual.columns
    assert 'distance' in actual.columns

    assert ptypes.is_datetime64_dtype(actual['date'])
    assert ptypes.is_float_dtype(actual['distance'])


def test_get_components():
    actual = T('bike', 1).component

    assert 'Component' == actual.name


@freeze_time('2100-02-28')
def test_get_components_foreign_key_object():
    obj = T('bike', 1).component
    actual = obj.components.all()

    assert 2 == len(actual)
    assert 'bike / Component / 2100-01-01 ... 2100-02-28' == str(actual[0])
    assert 'bike / Component / 2000-01-01 ... 2000-12-31' == str(actual[1])


def test_total_distance_full_for_bike():
    actual = T('bike', 1).total_distance()

    assert 60 == actual


def test_total_distance_one_day():
    actual = T('bike', 1).total_distance('2000-01-01', '2000-01-01')

    assert 10 == actual


@freeze_time('2100-02-28')
def test_components_list_first_component():
    actual = T('bike', 1).components_list

    actual = actual[0]

    assert datetime(2100, 1, 1).date() == actual['start_date']
    assert datetime(2100, 2, 28).date() == actual['end_date']
    assert 'whatewer' == actual['brand']
    assert 100 == actual['price']
    assert 30 == actual['km']


def test_components_list_last_component():
    actual = T('bike', 1).components_list

    actual = actual[1]

    assert datetime(2000, 1, 1).date() == actual['start_date']
    assert datetime(2000, 12, 31).date() == actual['end_date']
    assert 'unknown' == actual['brand']
    assert 10 == actual['price']
    assert 30 == actual['km']


def test_components_stats():
    actual = T('bike', 1).components_stats

    assert 15 == actual['avg']
    assert 15 == actual['median']


@pytest.mark.xfail(raises=Http404)
def test_component_not_exists():
    actual = T('bike', 10).component
