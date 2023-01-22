import pytest
from django.urls import resolve, reverse

from ..factories import BikeFactory, ComponentFactory
from .. import views

pytestmark = pytest.mark.django_db


def test_bike_info_index_func():
    view = resolve('/info/')

    assert views.bike_info_index is view.func


def test_bike_info_index_302(client_logged):
    url = reverse('bikes:info_index')
    response = client_logged.get(url)

    assert response.status_code == 302


def test_bike_info_index_no_records(client_logged):
    url = reverse('bikes:info_index')
    response = client_logged.get(url, follow=True)

    assert '<td class="bg-warning text-center" colspan="3">No records</td>' in str(
        response.content)


def test_bike_info_list_func():
    view = resolve('/xxx/info/')

    assert views.bike_info_lists is view.func


def test_bike_info_list_200(client_logged):
    url = reverse('bikes:info_list', kwargs={'bike_slug': 'xxx'})
    response = client_logged.get(url)

    assert response.status_code == 200


def test_bike_info_list_no_records(client_logged):
    url = reverse('bikes:info_list', kwargs={'bike_slug': 'xxx'})
    response = client_logged.get(url)

    assert '<td class="bg-warning text-center" colspan="3">No records</td>' in str(
        response.content)
