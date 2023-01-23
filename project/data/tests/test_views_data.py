import re
from datetime import date, timedelta

import pytest
from django.urls import resolve, reverse

from ...bikes.factories import BikeFactory
from ...core.lib.tests_utils import clean_content
from ...data.factories import DataFactory
from ...users.factories import UserFactory
from ...users.views import CustomLogin
from .. import views
from ..factories import DataFactory
from ..models import Data

pytestmark = pytest.mark.django_db


def test_data_detail_func():
    view = resolve('/data/detail/9/')

    assert views.DataDetail is view.func.view_class


def test_data_detail(client_logged):
    data = DataFactory()

    url = reverse('data:data_detail', kwargs={'pk': data.pk})
    response = client_logged.get(url)

    actual = response.context['object']
    assert response.status_code == 200
    assert actual == data


def test_data_detail_links(client_logged):
    data = DataFactory()

    url = reverse('data:data_detail', kwargs={'pk': data.pk})
    response = client_logged.get(url)

    actual = clean_content(response.content)

    row_id = f'row-id-{data.pk}'
    url_update = reverse('data:data_update', kwargs={'pk': data.pk})
    url_delete = reverse('data:data_delete', kwargs={'pk': data.pk})

    # table row
    assert f'<tr id="{row_id}" class="table-info" hx-target="this" hx-swap="outerHTML" hx-trigger="click[ctrlKey]" hx-get="{url_update}">' in actual
    # edit button
    assert f'<button type="button" class="btn btn-sm btn-warning" hx-get="{url_update}" hx-target="#{row_id}" hx-swap="outerHTML">' in actual
    # delete button
    assert f'<button type="button" class="btn btn-sm btn-danger" hx-get="{url_delete}" hx-target="#dialog" hx-swap="innerHTML">' in actual


def test_data_list_func():
    view = resolve('/data/list/')

    assert views.DataList is view.func.view_class


def test_data_list_not_loged(client):
    url = reverse('data:data_list')
    response = client.get(url, follow=True)

    assert response.resolver_match.func.view_class is CustomLogin


@pytest.mark.freeze_time('2000-01-31')
def test_data_list_user_items(client_logged):
    DataFactory()
    DataFactory(user=UserFactory(username='xxx'))

    url = reverse('data:data_list')

    response = client_logged.get(url)

    assert len(response.context['object_list']) == 1
    assert response.context['object_list'][0].user.username == 'bob'


def test_data_create_func():
    view = resolve('/data/create/')

    assert views.DataCreate is view.func.view_class


def test_data_create_not_loged(client):
    url = reverse('data:data_create')
    response = client.get(url, follow=True)
    assert response.resolver_match.func.view_class is CustomLogin


@pytest.mark.freeze_time('2000-2-2')
def test_data_create_load_form(client_logged):
    url = reverse('data:data_create')
    response = client_logged.get(url)
    content = clean_content(response.content)

    assert response.status_code == 200
    assert '<input type="text" name="date" value="2000-02-02"' in content


def test_data_create_data_valid(client_logged):
    bike = BikeFactory()
    data = {
        'bike': str(bike.id),
        'date': date(2000, 1, 1),
        'distance': 10.12,
        'time': timedelta(seconds=15),
        'temperature': 1.1,
        'ascent': 600,
        'descent': 500,
        'max_speed': 110,
        'cadence': 120,
        'heart_rate': 200,
    }
    url = reverse('data:data_create')
    response = client_logged.post(url, data=data)
    content = clean_content(response.content)

    assert '2000-01-01' in content
    assert '10.12' in content
    assert '0:00:15' in content
    assert '600' in content
    assert '500' in content
    assert '110' in content
    assert '120' in content
    assert '200' in content

    assert '<tr id="row-id-1"' in content
    assert 'hx-get="/data/delete/1/" hx-target="#dialog"' in content
    assert 'hx-get="/data/update/1/" hx-target="#row-id-1"' in content


def test_data_create_data_invalid(client_logged):
    url = reverse('data:data_create')
    response = client_logged.post(url, data={})

    form = response.context['form']
    assert not form.is_valid()
    assert 'bike' in form.errors
    assert 'date' in form.errors
    assert 'distance' in form.errors
    assert 'time' in form.errors


def test_data_delete_func():
    view = resolve('/data/delete/1/')

    assert views.DataDelete is view.func.view_class


def test_data_delete_not_loged(client):
    data = DataFactory()
    url = reverse('data:data_delete', kwargs={'pk': data.pk})
    response = client.get(url, follow=True)
    assert response.resolver_match.func.view_class is CustomLogin


def test_data_delete_200(client_logged):
    data = DataFactory()
    url = reverse('data:data_delete', kwargs={'pk': data.pk})

    response = client_logged.get(url)

    assert response.status_code == 200


def test_data_delete_404(client_logged):
    url = reverse('data:data_delete', kwargs={'pk': 99})
    response = client_logged.post(url)

    assert response.status_code == 404


def test_data_delete_load_form(client_logged):
    data = DataFactory()
    url = reverse('data:data_delete', kwargs={'pk': data.pk})

    response = client_logged.get(url)
    content = clean_content(response.content)

    res = re.findall(fr'<form.+hx-post="({url})"', content)
    assert res[0] == url
    assert f'<button type="submit" id="_delete" data-pk="{data.pk}"' in content


def test_data_delete(client_logged):
    obj = DataFactory()

    url = reverse('data:data_delete', kwargs={'pk': obj.pk})
    client_logged.post(url, {})

    assert  Data.objects.all().count() == 0


def test_data_update_func():
    view = resolve('/data/update/1/')

    assert views.DataUpdate is view.func.view_class


def test_data_update_not_loged(client):
    data = DataFactory()
    url = reverse('data:data_update', kwargs={'pk': data.pk})
    response = client.get(url, follow=True)
    assert response.resolver_match.func.view_class is CustomLogin


def test_data_update_object_200(client_logged):
    data = DataFactory()
    url = reverse('data:data_update', kwargs={'pk': data.pk})
    response = client_logged.get(url)

    assert response.status_code == 200


def test_data_update_object_404(client_logged):
    url = reverse('data:data_update', kwargs={'pk': 99})
    response = client_logged.get(url)

    assert response.status_code == 404


def test_data_update_loaded_form(client_logged):
    obj = DataFactory()
    url = reverse('data:data_update', kwargs={'pk': obj.pk})
    response = client_logged.get(url)
    content = clean_content(response.content)

    assert f'<option value="{obj.bike.pk}" selected>Short Name</option>' in content
    assert '<input type="text" name="date" value="2000-01-01"' in content
    assert '<input type="number" name="distance" value="10.0"' in content
    assert '<input type="text" name="time" value="00:16:40"' in content
    assert '<input type="number" name="temperature" value="10.0"' in content
    assert '<input type="number" name="ascent" value="100.0"' in content
    assert '<input type="number" name="descent" value="0.0"' in content
    assert '<input type="number" name="max_speed" value="15.0"' in content
    assert '<input type="number" name="heart_rate" value="140"' in content
    assert '<input type="number" name="cadence" value="85"' in content


def test_data_update(client_logged):
    obj = DataFactory()
    data = {
        'bike': str(obj.bike.id),
        'date': date(2000, 1, 1),
        'distance': 10.12,
        'time': timedelta(seconds=15),
        'temperature': 1.1,
        'ascent': 600,
        'descent': 500,
        'max_speed': 110,
        'cadence': 120,
        'heart_rate': 200,
    }

    url = reverse('data:data_update', kwargs={'pk': obj.pk})
    response = client_logged.post(url, data=data)
    content = clean_content(response.content)

    assert '2000-01-01' in content  # distance
    assert '10.12' in content  # distance
    assert '0:00:15' in content  # time
    assert '1.1' in content  # temperature
    assert '600' in content  # ascent
    assert '500' in content  # descent
    assert '110' in content  # max_speed
    assert '120' in content  # cadence
    assert '200' in content  # heart rate


def test_bike_quick_update_func():
    view = resolve('/data/quick_update/1/')

    assert views.QuickUpdate is view.func.view_class


def test_data_quick_update_not_loged(client):
    data = DataFactory()
    url = reverse('data:data_quick_update', kwargs={'pk': data.pk})
    response = client.get(url, follow=True)
    assert response.resolver_match.func.view_class is CustomLogin


def test_data_quick_update_404(client_logged):
    url = reverse('data:data_quick_update', kwargs={'pk': 99})
    response = client_logged.get(url)

    assert response.status_code == 404


def test_data_quick_update_200(client_logged):
    data = DataFactory()
    url = reverse('data:data_quick_update', kwargs={'pk': data.pk})
    response = client_logged.get(url)

    assert response.status_code == 200


def test_data_quick_update(client_logged):
    obj = DataFactory()

    assert obj.checked == 'n'

    url = reverse('data:data_quick_update', kwargs={'pk': obj.pk})

    client_logged.get(url)

    actual = Data.objects.get(pk=obj.pk)
    assert actual.checked == 'y'
