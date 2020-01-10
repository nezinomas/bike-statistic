from datetime import date

import pytest
from freezegun import freeze_time

from ...users.factories import UserFactory
from ..forms import BikeForm, ComponentForm, ComponentStatisticForm

pytestmark = pytest.mark.django_db


# ---------------------------------------------------------------------------------------
#                                                                                    Bike
# ---------------------------------------------------------------------------------------
def test_bike_init(get_user):
    BikeForm()


def test_bike_init_fields(get_user):
    form = BikeForm().as_p()

    assert '<input type="text" name="date"' in form
    assert '<input type="text" name="full_name"' in form
    assert '<input type="text" name="short_name"' in form

    assert '<select name="user"' not in form
    assert '<select name="slug"' not in form


@freeze_time('2001-01-01')
def test_bike_date_initial_value(get_user):
    UserFactory()

    form = BikeForm().as_p()

    assert '<input type="text" name="date" value="2001-01-01"' in form


def test_bike_valid_data(get_user):
    form = BikeForm(data={
        'date': '2000-01-01',
        'full_name': 'Full Name',
        'short_name': 'Short Name',
    })

    assert form.is_valid()

    data = form.save()

    assert data.date == date(2000, 1, 1)
    assert data.full_name == 'Full Name'
    assert data.short_name == 'Short Name'
    assert data.slug == 'short-name'
    assert data.user.username == 'bob'


def test_bike_blank_data(get_user):
    form = BikeForm(data={})

    assert not form.is_valid()

    assert len(form.errors) == 2
    assert 'date' in form.errors
    assert 'short_name' in form.errors
