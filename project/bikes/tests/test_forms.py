from datetime import date

import pytest
import time_machine
from django.forms.models import model_to_dict

from ...bikes.factories import BikeFactory, ComponentFactory
from ...users.factories import UserFactory
from ..forms import (BikeForm, BikeInfoForm, ComponentForm,
                     ComponentWearForm)

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
    assert '<input type="checkbox" name="main"' in form
    assert '<input type="checkbox" name="retired"' in form

    assert '<select name="user"' not in form
    assert '<select name="slug"' not in form


@time_machine.travel('2001-01-01')
def test_bike_date_initial_value(get_user):
    UserFactory()

    form = BikeForm().as_p()

    assert '<input type="text" name="date" value="2001-01-01"' in form


def test_bike_valid_data(get_user):
    form = BikeForm(data={
        'date': '2000-01-01',
        'full_name': 'Full Name',
        'short_name': 'Short Name',
        'main': True,
        'retired': False,
    })

    assert form.is_valid()

    data = form.save()

    assert data.date == date(2000, 1, 1)
    assert data.full_name == 'Full Name'
    assert data.short_name == 'Short Name'
    assert data.slug == 'short-name'
    assert data.user.username == 'bob'
    assert data.main


def test_bike_upate_turn_off_main(get_user):
    b = BikeFactory(main=True)
    b.short_name = 'xxxx'

    form = BikeForm(model_to_dict(b), instance=b)

    assert form.is_valid()

    data = form.save()

    assert data.short_name == 'xxxx'
    assert data.main


def test_bike_blank_data(get_user):
    form = BikeForm(data={})

    assert not form.is_valid()

    assert len(form.errors) == 2
    assert 'date' in form.errors
    assert 'short_name' in form.errors


def test_bike_main_only_one(get_user):
    BikeFactory(main=True)

    form = BikeForm(data={
        'date': '2000-01-01',
        'full_name': 'Full Name',
        'short_name': 'Short Name',
        'main': True,
    })

    assert not form.is_valid()


def test_bike_main_cant_be_retired(get_user):
    b = BikeFactory(main=True)
    b.retired = True

    form = BikeForm(model_to_dict(b), instance=b)

    assert not form.is_valid()


# ---------------------------------------------------------------------------------------
#                                                                               Bike Info
# ---------------------------------------------------------------------------------------
def test_bike_info_init(get_user):
    BikeInfoForm()


def test_bike_info_init_fields(get_user):
    form = BikeInfoForm().as_p()

    assert '<input type="text" name="component"' in form
    assert '<input type="text" name="description"' in form


def test_bike_info_valid_data(get_user):
    bike = BikeFactory()

    form = BikeInfoForm(data={
        'component': 'Component',
        'description': 'Description',
    }, **{'bike_slug': bike.slug})

    assert form.is_valid()

    data = form.save()

    assert data.component == 'Component'
    assert data.description == 'Description'
    assert data.bike.short_name == 'Short Name'


def test_bike_info_blank_data(get_user):
    form = BikeInfoForm(data={})

    assert not form.is_valid()

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


# ---------------------------------------------------------------------------------------
#                                                                          Component Wear
# ---------------------------------------------------------------------------------------
def test_component_statistic_init(get_user):
    ComponentWearForm()


def test_component_statistic_init_fields(get_user):
    form = ComponentWearForm().as_p()

    assert '<input type="text" name="start_date"' in form
    assert '<input type="text" name="end_date"' in form
    assert '<input type="number" name="price"' in form
    assert '<input type="text" name="brand"' in form


def test_component_statistic_valid_data(get_user):
    b = BikeFactory()
    c = ComponentFactory()

    form = ComponentWearForm(data={
        'start_date': '2000-01-01',
        'end_date': '2000-01-31',
        'price': 10.01,
        'brand': 'Brand',
        'bike': b.pk,
        'component': c.pk,
    }, **{'bike_slug': b.slug, 'component_pk': c.pk})

    assert form.is_valid()

    data = form.save()

    assert data.start_date == date(2000, 1, 1)
    assert data.end_date == date(2000, 1, 31)
    assert data.price == 10.01
    assert data.brand == 'Brand'
    assert data.bike == b
    assert data.component == c


def test_component_statistic_blank_data(get_user):
    form = ComponentWearForm(data={})

    assert not form.is_valid()

    assert 'start_date' in form.errors


def test_wear_end_date_earlier_than_start_date():
    b = BikeFactory()
    c = ComponentFactory()

    form = ComponentWearForm(data={
        'start_date': '2000-01-31',
        'end_date': '2000-01-01',
        'price': 10.01,
        'brand': 'Brand',
        'bike': b.pk,
        'component': c.pk,
    }, **{'bike_slug': b.slug, 'component_pk': c.pk})

    assert not form.is_valid()

    assert 'end_date' in form.errors
    assert 'End date cannot be earlier than start date.' in form.errors["end_date"]