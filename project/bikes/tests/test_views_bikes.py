import pytest
from django.urls import resolve, reverse

from ...bikes.factories import BikeFactory, ComponentFactory
from ...core.lib.tests_utils import clean_content
from .. import views

pytestmark = pytest.mark.django_db


def test_bike_list_func():
    view = resolve('/bike/')

    assert views.BikeList is view.func.view_class


def test_bike_detail_func():
    view = resolve('/bike/detail/9/')

    assert views.BikeDetail is view.func.view_class


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
