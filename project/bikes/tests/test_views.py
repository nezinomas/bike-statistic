import pytest
from django.urls import resolve, reverse

from .. import views

pytestmark = pytest.mark.django_db


# ---------------------------------------------------------------------------------------
#                                                                               bike list
# ---------------------------------------------------------------------------------------
def test_bike_list_func():
    view = resolve('/bike/')

    assert views.bike.lists == view.func


def test_bike_list_200_no_data(client_logged):
    url = reverse('bikes:bike_list')
    response = client_logged.get(url)

    assert response.status_code == 200


def test_bike_list_200(client_logged):
    url = reverse('bikes:bike_list')
    response = client_logged.get(url)

    assert response.status_code == 200


def test_bike_list_no_records(client_logged):
    url = reverse('bikes:bike_list')
    response = client_logged.get(url)

    assert '<td class="bg-warning text-center" colspan="4">No records</td>' in str(
        response.content)
