from datetime import date

import pytest
from django.urls import resolve, reverse
from ...users.factories import UserFactory
from ...bikes.factories import BikeFactory
from ...core.lib.tests_utils import clean_content
from .. import models, views

pytestmark = pytest.mark.django_db


def test_bike_list_func():
    view = resolve('/bike/')

    assert views.BikeList is view.func.view_class


def test_bike_detail_func():
    view = resolve('/bike/detail/9/')

    assert views.BikeDetail is view.func.view_class


def test_bike_create_func():
    view = resolve('/bike/create/')

    assert views.BikeCreate is view.func.view_class


def test_bike_list_200(client_logged):
    url = reverse('bikes:bike_list')
    response = client_logged.get(url)

    assert response.status_code == 200


def test_bike_list_no_records(client_logged):
    url = reverse('bikes:bike_list')
    response = client_logged.get(url)

    assert '<td class="bg-warning text-center" colspan="4">No records</td>' in str(
        response.content)


def test_bike_list(client_logged):
    bike = BikeFactory()

    url = reverse('bikes:bike_list')
    response = client_logged.get(url)
    content = clean_content(response.content)
    info_url = reverse("bikes:info_list", kwargs={"bike_slug": bike.slug})

    assert '1999-01-01' in content
    assert 'Full Name' in content
    assert f'<a href="{info_url}">Short Name</a>' in content


def test_bike_detail(client_logged):
    bike = BikeFactory()

    url = reverse('bikes:bike_detail', kwargs={'pk': bike.pk})
    response = client_logged.get(url)

    actual = response.context['object']
    assert response.status_code == 200
    assert actual == bike


def test_bike_detail_links(client_logged):
    bike = BikeFactory()

    url = reverse('bikes:bike_detail', kwargs={'pk': bike.pk})
    response = client_logged.get(url)

    actual = clean_content(response.content)

    row_id = f'row-id-{bike.pk}'
    url_update = reverse('bikes:bike_update', kwargs={'pk': bike.pk})
    url_delete = reverse('bikes:bike_delete', kwargs={'pk': bike.pk})

    # table row
    assert f'<tr id="{row_id}" hx-target="this" hx-swap="outerHTML" hx-trigger="click[ctrlKey]" hx-get="{url_update}">' in actual
    # edit button
    assert f'<button type="button" class="btn btn-sm btn-warning" hx-get="{url_update}" hx-target="#{row_id}" hx-swap="outerHTML">' in actual
    # delete button
    assert f'<button type="button" class="btn btn-sm btn-danger" hx-get="{url_delete}" hx-target="#dialog" hx-swap="innerHTML">' in actual


@pytest.mark.freeze_time('2000-2-2')
def test_bike_create_load_form(client_logged):
    url = reverse('bikes:bike_create')
    response = client_logged.get(url)
    content = clean_content(response.content)

    assert response.status_code == 200
    assert '<input type="text" name="date" value="2000-02-02"' in content


def test_bike_create_save_with_valid_data(client_logged):
    user = UserFactory()

    data = {
        'date': '2000-2-2',
        'full_name': 'Full Name',
        'short_name': 'Short Name',
        'main': 'True'
    }

    url = reverse('bikes:bike_create')
    client_logged.post(url, data)
    actual = models.Bike.objects.first()

    assert actual.date == date(2000, 2, 2)
    assert actual.full_name == 'Full Name'
    assert actual.short_name == 'Short Name'
    assert actual.user == user
    assert actual.main is True
    assert actual.retired is False


def test_bike_create_save_form_errors(client_logged):
    data = {}
    url = reverse('bikes:bike_create')
    response = client_logged.post(url, data)
    form = response.context['form']
    assert not form.is_valid()
    assert 'date' in form.errors
    assert 'short_name' in form.errors
