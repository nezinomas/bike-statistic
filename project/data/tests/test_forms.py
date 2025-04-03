from datetime import date, timedelta

import pytest

from ...bikes.factories import BikeFactory
from ...users.factories import UserFactory
from ..forms import DataForm, DateFilterForm

pytestmark = pytest.mark.django_db


# -------------------------------------------------------------------------------------
#                                                                           Filter Form
# -------------------------------------------------------------------------------------
def test_date_filter_form_is_valid():
    data = {"start_date": "2000-01-01", "end_date": "2000-01-31"}
    form = DateFilterForm(data=data)

    assert form.is_valid()


def test_date_filter_form_invalid():
    form = DateFilterForm(data={"start_date": "xxx", "end_date": "xxx"})

    assert not form.is_valid()


# -------------------------------------------------------------------------------------
#                                                                             Data Form
# -------------------------------------------------------------------------------------
def test_data_form_data_valid(get_user):
    bike = BikeFactory()
    data = {
        "bike": str(bike.id),
        "date": date(2000, 1, 1),
        "distance": 10.12,
        "time": timedelta(seconds=15),
        "temperature": 1.1,
        "ascent": 600,
        "descent": 500,
        "max_speed": 110,
        "cadence": 120,
        "heart_rate": 200,
    }
    form = DataForm(data=data)

    assert form.is_valid()


def test_data_form_data_invalid(get_user):
    form = DataForm(data={})

    assert not form.is_valid()
    assert "bike" in form.errors
    assert "date" in form.errors
    assert "distance" in form.errors
    assert "time" in form.errors


def test_data_bike_current_user(get_user):
    u = UserFactory(username="xxx")

    BikeFactory(short_name="T1")  # user bob, current user
    BikeFactory(short_name="T2", user=u)  # user xxx

    form = DataForm().as_p()

    assert "T1" in form
    assert "T2" not in form


def test_retired_bike_not_in_form(get_user):
    BikeFactory(short_name="T1")
    BikeFactory(short_name="T2", retired=True)

    form = DataForm().as_p()

    assert "T1" in form
    assert "T2" not in form
