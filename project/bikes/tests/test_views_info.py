import pytest
from django.urls import resolve, reverse

from ...core.lib.tests_utils import clean_content
from .. import models, views
from ..factories import BikeFactory, BikeInfoFactory

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


def test_info_index(client_logged):
    BikeInfoFactory()

    url = reverse('bikes:info_index')
    response = client_logged.get(url, follow=True)

    assert response.status_code == 200
    assert response.resolver_match.func.view_class is views.BikeInfoList


def test_info_list_func():
    view = resolve('/info/xxx/')

    assert views.BikeInfoList is view.func.view_class


def test_info_list_200(client_logged):
    url = reverse('bikes:info_list', kwargs={'bike_slug': 'xxx'})
    response = client_logged.get(url)

    assert response.status_code == 200


def test_info_list_context(client_logged):
    info = BikeInfoFactory()
    url = reverse('bikes:info_list', kwargs={'bike_slug': info.bike.slug})
    response = client_logged.get(url)
    context = response.context

    assert 'object_list' in context
    assert 'bike_list' in context


def test_info_list_no_records(client_logged):
    url = reverse('bikes:info_list', kwargs={'bike_slug': 'xxx'})
    response = client_logged.get(url)

    assert '<td class="bg-warning text-center" colspan="3"> No records </td>' in str(response.content)


def test_info_list_with_data(client_logged):
    info = BikeInfoFactory()

    url = reverse('bikes:info_list', kwargs={'bike_slug': info.bike.slug})
    response = client_logged.get(url)
    content = clean_content(response.content)

    assert 'Component' in content
    assert 'Description' in content


def test_info_list_with_data(client_logged):
    info = BikeInfoFactory()
    BikeInfoFactory(component="XXX", description="YYY", bike=BikeFactory(short_name='z'))

    url = reverse('bikes:info_list', kwargs={'bike_slug': info.bike.slug})
    response = client_logged.get(url)
    content = clean_content(response.content)

    assert 'Component' in content
    assert 'Description' in content
    assert 'XXX' not in content
    assert 'YYY' not in content


def test_info_list_with_data_links(client_logged):
    info = BikeInfoFactory()

    url = reverse('bikes:info_list', kwargs={'bike_slug': info.bike.slug})
    response = client_logged.get(url)
    actual = clean_content(response.content)

    row_id = f'row-id-{info.pk}'
    url_update = reverse('bikes:info_update', kwargs={'bike_slug': info.bike.slug, 'pk': info.pk})
    url_delete = reverse('bikes:info_delete', kwargs={'bike_slug': info.bike.slug, 'pk': info.pk})

    # table row
    assert f'<tr id="{row_id}" hx-target="this" hx-swap="outerHTML" hx-trigger="click[ctrlKey]" hx-get="{url_update}">' in actual
    # edit button
    assert f'<button type="button" class="btn btn-sm btn-warning" hx-get="{url_update}" hx-target="#{row_id}" hx-swap="outerHTML">' in actual
    # delete button
    assert f'<button type="button" class="btn btn-sm btn-danger" hx-get="{url_delete}" hx-target="#dialog" hx-swap="innerHTML">' in actual
