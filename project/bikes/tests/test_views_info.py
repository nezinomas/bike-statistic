import re
import pytest
from django.urls import resolve, reverse

from ...core.lib.tests_utils import clean_content
from .. import models, views
from ..factories import BikeFactory, BikeInfoFactory

pytestmark = pytest.mark.django_db


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


def test_info_list_no_records(client_logged):
    url = reverse('bikes:info_list', kwargs={'bike_slug': 'xxx'})
    response = client_logged.get(url)

    assert '<div class="alert alert-warning">No records</div>' in str(response.content)


def test_info_list_with_data(client_logged):
    info = BikeInfoFactory()

    url = reverse('bikes:info_list', kwargs={'bike_slug': info.bike.slug})
    response = client_logged.get(url)
    content = clean_content(response.content)

    assert 'Component' in content
    assert 'Description' in content


def test_info_list_two_bikes(client_logged):
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

    url_update = reverse('bikes:info_update', kwargs={'bike_slug': info.bike.slug, 'pk': info.pk})
    url_delete = reverse('bikes:info_delete', kwargs={'bike_slug': info.bike.slug, 'pk': info.pk})

    # table row
    assert f'<tr hx-target="#mainModal" hx-trigger="dblclick" hx-get="{url_update}"' in actual
    # edit button
    assert f'<button type="button" class="btn-secondary btn-edit" hx-get="{url_update}" hx-target="#mainModal"' in actual
    # delete button
    assert f'<button type="button" class="btn-trash" hx-get="{url_delete}" hx-target="#mainModal"' in actual


def test_info_create_func():
    view = resolve('/info/bike/create/')

    assert views.BikeInfoCreate is view.func.view_class


def test_info_create_load_form(client_logged):
    bike = BikeFactory()
    url = reverse('bikes:info_create', kwargs={'bike_slug': bike.slug})
    response = client_logged.get(url)

    assert response.status_code == 200


def test_info_create_save_with_valid_data(client_logged):
    bike = BikeFactory()

    data = {
        'component': 'Component',
        'description': 'Description',
    }

    url = reverse('bikes:info_create', kwargs={'bike_slug': bike.slug})
    client_logged.post(url, data)
    actual = models.BikeInfo.objects.first()

    assert actual.component == 'Component'
    assert actual.description == 'Description'
    assert actual.bike == bike


def test_info_create_save_form_errors(client_logged):
    bike = BikeFactory()
    data = {}
    url = reverse('bikes:info_create', kwargs={'bike_slug': bike.slug})
    response = client_logged.post(url, data)
    form = response.context['form']

    assert not form.is_valid()
    assert 'component' in form.errors
    assert 'description' in form.errors


def test_info_update_func():
    view = resolve('/info/bike/update/1/')

    assert views.BikeInfoUpdate is view.func.view_class


def test_info_update_load_form(client_logged):
    info = BikeInfoFactory()

    url = reverse('bikes:info_update', kwargs={'bike_slug': info.bike.slug, 'pk': info.pk})
    response = client_logged.get(url)
    form = response.context['form'].as_p()

    assert 'Component' in form
    assert 'Description' in form


def test_info_update_component(client_logged):
    info = BikeInfoFactory()

    data = {
        'component': 'XXX',
        'description': info.description,
    }

    url = reverse('bikes:info_update', kwargs={'bike_slug': info.bike.slug, 'pk': info.pk})
    client_logged.post(url, data)

    actual = models.BikeInfo.objects.get(pk=info.pk)

    assert actual.component == 'XXX'
    assert actual.description == info.description
    assert actual.bike == info.bike


def test_info_update_description(client_logged):
    info = BikeInfoFactory()

    data = {
        'component': info.component,
        'description': 'XXX',
    }

    url = reverse('bikes:info_update', kwargs={'bike_slug': info.bike.slug, 'pk': info.pk})
    client_logged.post(url, data)

    actual = models.BikeInfo.objects.get(pk=info.pk)

    assert actual.component == info.component
    assert actual.description == 'XXX'
    assert actual.bike == info.bike


def test_info_delete_func():
    view = resolve('/info/bike/delete/1/')

    assert views.BikeInfoDelete is view.func.view_class


def test_info_delete_200(client_logged):
    info = BikeInfoFactory()
    url = reverse('bikes:info_delete', kwargs={'bike_slug': info.bike.slug, 'pk': info.pk})

    response = client_logged.get(url)

    assert response.status_code == 200


def test_info_delete_load_form(client_logged):
    info = BikeInfoFactory()
    url = reverse('bikes:info_delete', kwargs={'bike_slug': info.bike.slug, 'pk': info.pk})

    response = client_logged.get(url)
    content = clean_content(response.content)
    res = re.findall(fr'<form.+hx-post="({url})"', content)
    assert res[0] == url
    assert f'<button type="submit" id="_delete" data-pk="{info.pk}"' in content


def test_info_delete(client_logged):
    info = BikeInfoFactory()
    url = reverse('bikes:info_delete', kwargs={'bike_slug': info.bike.slug, 'pk': info.pk})

    client_logged.post(url, {})

    assert models.BikeInfo.objects.all().count() == 0
