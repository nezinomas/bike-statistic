import pytest
from django.urls import resolve, reverse

from ..factories import BikeFactory, ComponentFactory
from .. import views

pytestmark = pytest.mark.django_db


def test_info_index_func():
    view = resolve('/info/')

    assert views.BikeInfoIndex is view.func.view_class


def test_info_index_302(client):
    url = reverse('bikes:info_index')
    response = client.get(url)

    assert response.status_code == 302


def test_info_index_no_records(client_logged):
    url = reverse('bikes:info_index')
    response = client_logged.get(url, follow=True)

    assert response.status_code == 200
    assert response.resolver_match.func.view_class is views.BikeList


# def test_info_list_func():
#     view = resolve('/xxx/info/')

#     assert views.bike_info_lists is view.func


# def test_info_list_200(client_logged):
#     url = reverse('bikes:info_list', kwargs={'bike_slug': 'xxx'})
#     response = client_logged.get(url)

#     assert response.status_code == 200


# def test_info_list_no_records(client_logged):
#     url = reverse('bikes:info_list', kwargs={'bike_slug': 'xxx'})
#     response = client_logged.get(url)

#     assert '<td class="bg-warning text-center" colspan="3">No records</td>' in str(
#         response.content)
