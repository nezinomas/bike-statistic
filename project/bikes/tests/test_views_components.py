import pytest
from django.urls import resolve, reverse

from ...bikes.factories import ComponentFactory
from ...core.lib.tests_utils import clean_content
from .. import views

pytestmark = pytest.mark.django_db


def test_component_list_func():
    view = resolve('/component/')

    assert views.ComponentList is view.func.view_class


def test_component_list_302(client):
    url = reverse('bikes:component_list')
    response = client.get(url)

    assert response.status_code == 302


def test_component_list_200(client_logged):
    url = reverse('bikes:component_list')
    response = client_logged.get(url)

    assert response.status_code == 200


def test_component_list_no_records(client_logged):
    url = reverse('bikes:component_list')
    response = client_logged.get(url)

    assert '<td class="text-center bg-warning" colspan="3"> No components </td>' in str(
        response.content)


def test_component_list(client_logged):
    ComponentFactory()

    url = reverse('bikes:component_list')
    response = client_logged.get(url)
    content = clean_content(response.content)

    assert 'Component' in content

