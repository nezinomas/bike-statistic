from datetime import datetime, timedelta

import pandas as pd
import pandas.api.types as ptypes
import pytest

from ...core.factories import (ComponentFactory, ComponentStatisticFactory,
                               DataFactory)
from ..helpers.view_stats_helper import Filter as T

pytestmark = pytest.mark.django_db


@pytest.fixture(scope='module', autouse=True)
def components(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        ComponentFactory()


@pytest.fixture(scope='module', autouse=True)
def data(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        d1 = DataFactory(
            date=datetime(2000, 1, 1).date(),
            distance=10.0,
            time=timedelta(seconds=1000),
            temperature=10,
            ascent=100
        )
        d2 = DataFactory(
            date=datetime(2000, 1, 31).date(),
            distance=20.0,
            time=timedelta(seconds=2000),
            temperature=20,
            ascent=200
        )
    yield
    with django_db_blocker.unblock():
        d1.delete()
        d2.delete()



def test_get_df():
    actual = T('xbike', 1)._Filter__df

    assert 2 == len(actual)

    assert 'date' in actual.columns
    assert 'distance' in actual.columns

    assert ptypes.is_datetime64_dtype(actual['date'])
    assert ptypes.is_float_dtype(actual['distance'])
