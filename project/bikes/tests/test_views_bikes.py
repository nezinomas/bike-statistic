import pytest
from django.urls import resolve, reverse

from ...bikes.factories import BikeFactory, ComponentFactory
from ...core.lib.tests_utils import clean_content
from .. import views

pytestmark = pytest.mark.django_db


def test_bike_list_func():
    view = resolve('/bike/')

    assert views.BikeList is view.func.view_class


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

