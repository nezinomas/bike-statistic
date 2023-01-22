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


def test_component_detail_func():
    view = resolve('/component/detail/9/')

    assert views.ComponentDetail is view.func.view_class


def test_component_detail(client_logged):
    comp = ComponentFactory()

    url = reverse('bikes:component_detail', kwargs={'pk': comp.pk})
    response = client_logged.get(url)

    actual = response.context['object']
    assert response.status_code == 200
    assert actual == comp


def test_component_detail_links(client_logged):
    comp = ComponentFactory()

    url = reverse('bikes:component_detail', kwargs={'pk': comp.pk})
    response = client_logged.get(url)

    actual = clean_content(response.content)

    row_id = f'row-id-{comp.pk}'
    url_update = reverse('bikes:component_update', kwargs={'pk': comp.pk})
    url_delete = reverse('bikes:component_delete', kwargs={'pk': comp.pk})

    # table row
    assert f'<tr id="{row_id}" hx-target="this" hx-swap="outerHTML" hx-trigger="click[ctrlKey]" hx-get="{url_update}">' in actual
    # edit button
    assert f'<button type="button" class="btn btn-sm btn-warning" hx-get="{url_update}" hx-target="#{row_id}" hx-swap="outerHTML">' in actual
    # delete button
    assert f'<button type="button" class="btn btn-sm btn-danger" hx-get="{url_delete}" hx-target="#dialog" hx-swap="innerHTML">' in actual
