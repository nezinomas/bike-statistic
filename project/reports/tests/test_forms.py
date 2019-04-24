from datetime import datetime, timedelta

import pytest

from ...core.factories import BikeFactory
from ..forms import DataForm, DateFilterForm


def test_date_filter_form_is_valid():
    form = DateFilterForm(
        data={
            'start_date': '2000-01-01',
            'end_date': '2000-01-31'
        }
    )
    assert form.is_valid()


def test_date_filter_form_invalid():
    form = DateFilterForm(
        data={
            'start_date': 'xxx',
            'end_date': 'xxx'
        }
    )
    assert not form.is_valid()


def test_date_filter_form_invalid_start_bigger_than_end():
    form = DateFilterForm(
        data={
            'start_date': '2000-01-31',
            'end_date': '2000-01-01'
        }
    )
    assert not form.is_valid()


@pytest.mark.django_db
def test_data_form_is_valid():
    bike = BikeFactory()
    form = DataForm(
        data={
            'bike': str(bike.id),
            'date': datetime(2000, 1, 1),
            'distance': 10.12,
            'time': timedelta(seconds=15),
            'temperature': 0.0,
            'ascent': 0.0,
            'descent': 0.0,
            'max_speed': 0.0,
            'cadence': 0,
            'heart_rate': 0,
            'checked': 'y'
        }
    )
    assert form.is_valid()
