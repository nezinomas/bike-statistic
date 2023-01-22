import re

import pytest
from django.urls import resolve, reverse

from ...bikes.factories import ComponentFactory
from ...core.lib.tests_utils import clean_content
from ...users.factories import UserFactory
from .. import models, views

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


def test_component_create_func():
    view = resolve('/component/create/')

    assert views.ComponentCreate is view.func.view_class


def test_component_create_load_form(client_logged):
    url = reverse('bikes:component_create')
    response = client_logged.get(url)
    content = clean_content(response.content)

    assert response.status_code == 200
    assert '<tr id="form-row">' in content
    assert '<form method="post" novalidate>' in content

    button_create = re.findall(fr'<button.+hx-post="({url})" hx-target="(.*?)"', content)
    assert button_create[0][0] == url
    assert button_create[0][1] == '#form-row'


def test_component_create_save_with_valid_data(client_logged):
    user = UserFactory()
    data = {'name': 'Full Name'}

    url = reverse('bikes:component_create')
    client_logged.post(url, data)
    actual = models.Component.objects.first()

    assert actual.name == 'Full Name'
    assert actual.user == user


def test_component_create_save_form_errors(client_logged):
    data = {}
    url = reverse('bikes:component_create')
    response = client_logged.post(url, data)
    form = response.context['form']
    assert not form.is_valid()
    assert 'name' in form.errors
