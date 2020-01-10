from datetime import date

import pytest
from freezegun import freeze_time

from ...bikes.factories import BikeFactory
from ...users.factories import UserFactory
from ..forms import (BikeForm, BikeInfoForm, ComponentForm,
                     ComponentStatisticForm)

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


# ---------------------------------------------------------------------------------------
#                                                                               Bike Info
# ---------------------------------------------------------------------------------------
def test_bike_info_init(get_user):
    BikeInfoForm()


def test_bike_info_init_fields(get_user):
    form = BikeInfoForm().as_p()

    assert '<input type="text" name="component"' in form
    assert '<input type="text" name="description"' in form
    assert '<input type="hidden" name="bike"' in form


def test_bike_info_valid_data(get_user):
    b = BikeFactory()

    form = BikeInfoForm(data={
        'component': 'Component',
        'description': 'Description',
        'bike': b.pk,
    })

    assert form.is_valid()

    data = form.save()

    assert data.component == 'Component'
    assert data.description == 'Description'
    assert data.bike.short_name == 'Short Name'


def test_bike_info_blank_data(get_user):
    form = BikeInfoForm(data={})

    assert not form.is_valid()

    assert len(form.errors) == 3
    assert 'bike' in form.errors
    assert 'component' in form.errors
    assert 'description' in form.errors


# ---------------------------------------------------------------------------------------
#                                                                               Component
# ---------------------------------------------------------------------------------------
def test_component_init(get_user):
    ComponentForm()


def test_component_init_fields(get_user):
    form = ComponentForm().as_p()

    assert '<input type="text" name="name"' in form
    assert '<select name="user"' not in form


def test_component_valid_data(get_user):
    form = ComponentForm(data={
        'name': 'Component',
    })

    assert form.is_valid()

    data = form.save()

    assert data.name == 'Component'
    assert data.user.username == 'bob'


def test_component_blank_data(get_user):
    form = ComponentForm(data={})

    assert not form.is_valid()

    assert len(form.errors) == 1
    assert 'name' in form.errors
