from datetime import date

import pytest

from ...data.factories import DataFactory
from ...data.models import Data
from ..factories import (BikeFactory, ComponentFactory,
                         ComponentStatisticFactory)
from ..lib.stats import ComponentWear
from ..models import ComponentStatistic

pytestmark = pytest.mark.django_db


@pytest.fixture()
def _stats(get_user):
    b = BikeFactory()
    c = ComponentFactory()

    ComponentStatisticFactory()
    ComponentStatisticFactory(
        start_date=date(2000, 1, 1),
        end_date=None,
        price=100,
        brand='whatewer'
    )
    ComponentStatisticFactory(
        bike=BikeFactory(short_name='XXX')
    )

    qs = (
        ComponentStatistic.objects
        .items()
        .filter(bike__slug=b.slug, component__pk=c.pk)
    )

    return qs


@pytest.fixture()
def _data(get_user):
    b = BikeFactory()

    DataFactory(date=date(1999, 1, 1), distance=10.5)
    DataFactory(date=date(1999, 1, 31), distance=11.5)
    DataFactory(date=date(2000, 1, 31), distance=12.5)

    qs = (
        Data.objects
        .items()
        .filter(bike__slug=b.slug)
    )

    return qs


def test_total_bike_distance(_stats, _data):
    actual = ComponentWear(_stats, _data).bike_km

    assert actual == 34.5


def test_component_distance(_stats, _data):
    expect = {1: 22.0, 2: 12.5}
    actual = ComponentWear(_stats, _data).component_km

    assert expect == actual


def test_component_distance_no_data(_stats):
    expect = {1: 0, 2: 0}
    actual = ComponentWear(_stats, []).component_km

    assert expect == actual

def test_component_distance_no_components():
    expect = {}
    actual = ComponentWear([], []).component_km

    assert expect == actual


def test_component_stats(_stats, _data):
    actual = ComponentWear(_stats, _data).component_stats

    assert actual['avg'] == 17.25
    assert actual['median'] == 17.25


def test_component_stats_no_datea(_stats):
    actual = ComponentWear(_stats, []).component_stats

    assert actual['avg'] == 0
    assert actual['median'] == 0


def test_component_stats_no_components():
    actual = ComponentWear([], []).component_stats

    assert actual['avg'] == 0
    assert actual['median'] == 0
