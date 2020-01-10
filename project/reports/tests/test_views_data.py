import json

import pytest
from django.urls import resolve, reverse
from freezegun import freeze_time

from ...reports.factories import DataFactory
from ...core.helpers.test_helpers import login_rediretion
from ...users.factories import UserFactory
from ..factories import DataFactory
from ..models import Data
from ..views import data, data_list

pytestmark = pytest.mark.django_db


def last_id():
    return Data.objects.values_list('id', flat=True)[0]


# ---------------------------------------------------------------------------------------
#                                                                               data_list
# ---------------------------------------------------------------------------------------
def test_data_list_not_loged(client, jan_2000):
    login_rediretion(client, 'reports:data_list', kwargs=jan_2000)


def test_data_list_valid_date(client, login, jan_2000):
    url = reverse('reports:data_list', kwargs=jan_2000)
    response = client.get(url)

    assert '<form class="filter"' in str(response.content)
    assert 'bob' in str(response.content)


def test_data_list_not_valid_date_01(client):
    response = client.get('/data/2000/2001/')
    assert response.status_code == 404


def test_data_list_not_valid_date_02(client):
    response = client.get('/data/xxxx-xx-xx/xxxx-xx-xx/')
    assert response.status_code == 404


def test_data_list_date_filter_redirection(client, login, jan_2000):
    url = reverse('reports:data_list', kwargs=jan_2000)
    data_ = {**jan_2000, 'date_filter': True}
    response = client.post(url, data=data_, follow=True)

    assert response.status_code == 200
    assert data_list == resolve(response.redirect_chain[0][0]).func

    assert (
        '<input type="text" name="start_date" value="2000-01-01"'
        in str(response.content)
    )
    assert (
        '<input type="text" name="end_date" value="2000-01-31"'
        in str(response.content)
    )


def test_data_list_user_items(client_logged, jan_2000):
    DataFactory()
    DataFactory(user=UserFactory(username='xxx'))

    url = reverse('reports:data_list', kwargs=jan_2000)
    data_ = {**jan_2000, 'date_filter': True}
    response = client_logged.post(url, data=data_, follow=True)

    assert len(response.context['objects']) == 1
    assert response.context['objects'][0].user.username == 'bob'


# ---------------------------------------------------------------------------------------
#                                                                            data_partial
# ---------------------------------------------------------------------------------------
def test_data_partial_not_loged(client):
    login_rediretion(
        client,
        'reports:data_partial',
        kwargs={'start_date': '2000-01-01'}
    )


@freeze_time("1999-01-15")
def test_data_partial_redirection(client, login):
    response = client.get('/data/1999-01-01/', follow=True)

    assert response.status_code == 200
    assert response.resolver_match.url_name == 'data_list'


@freeze_time("1999-01-15")
def test_data_partial_func(client):
    view = resolve('/data/1999-01-01/')
    assert data.data_partial == view.func


# ---------------------------------------------------------------------------------------
#                                                                              data_empty
# ---------------------------------------------------------------------------------------
def test_data_empty_not_loged(client):
    login_rediretion(client, 'reports:data_empty')


@freeze_time("1999-01-15")
def test_data_empty_redirection(client, login):
    response = client.get('/data/', follow=True)

    assert response.status_code == 200
    assert response.resolver_match.url_name == 'data_list'


@freeze_time("1999-01-15")
def test_data_empty_func(client):
    view = resolve('/data/')
    assert data.data_empty == view.func


# ---------------------------------------------------------------------------------------
#                                                                                   index
# ---------------------------------------------------------------------------------------
def test_index_not_loged(client):
    login_rediretion(client, 'reports:index')


@freeze_time("1999-01-15")
def test_index_redirection(client, login):
    response = client.get('/', follow=True)

    assert response.status_code == 200
    assert response.resolver_match.url_name == 'data_list'


@freeze_time("1999-01-15")
def test_index_func(client):
    view = resolve('/')
    assert data.index == view.func


# ---------------------------------------------------------------------------------------
#                                                                             data_create
# ---------------------------------------------------------------------------------------
def test_data_create_not_loged(client, jan_2000):
    login_rediretion(client, 'reports:data_create', kwargs=jan_2000)


def test_data_create_form_valid(client, login, post_data, jan_2000):
    url = reverse('reports:data_create', kwargs=jan_2000)
    response = client.post(url, data=post_data)
    actual = json.loads(response.content)
    content = actual['html_list']

    assert actual['form_is_valid']
    assert '<td class="text-center">2000-01-01' in content
    assert '<td class="text-center">10.12</td>' in content
    assert '<td class="text-center">0:00:15</td>' in content

    id_ = last_id()
    row = '<tr id="row_id_{0}" data-pk="{0}"'
    update = 'data-url="/api/data/2000-01-01/2000-01-31/update/{0}/"'
    delete = 'data-url="/api/data/2000-01-01/2000-01-31/delete/{0}/"'

    assert row.format(id_) in content
    assert update.format(id_) in content
    assert delete.format(id_) in content


def test_data_create_form_invalid(client, login, jan_2000):
    url = reverse('reports:data_create', kwargs=jan_2000)
    response = client.post(url, data={})
    actual = json.loads(response.content)

    assert not actual['form_is_valid']


# ---------------------------------------------------------------------------------------
#                                                                             data_delete
# ---------------------------------------------------------------------------------------
def test_data_delete_not_loged(client, jan_2000):
    login_rediretion(client, 'reports:data_delete', kwargs={**jan_2000, 'pk': 99})


def test_data_delete(client, login, jan_2000):
    obj = DataFactory()

    url = reverse('reports:data_delete', kwargs={**jan_2000, 'pk': obj.pk})
    response = client.post(url)

    actual = json.loads(response.content)

    assert actual['form_is_valid']
    assert not Data.objects.items()


def test_data_delete_404(client, login, jan_2000):
    url = reverse('reports:data_delete', kwargs={**jan_2000, 'pk': 99})
    response = client.post(url)

    assert response.status_code == 404


def test_data_delete_load_confirm_form(client, login, jan_2000):
    obj = DataFactory()
    url = reverse('reports:data_delete', kwargs={**jan_2000, 'pk': obj.pk})
    response = client.get(url)

    actual = json.loads(response.content)

    url = f'<form method="post" action="{url}"'
    msg = f'Are you sure you want to delete record: <strong>{obj}</strong>?'

    assert url in actual['html_form']
    assert msg in actual['html_form']


# ---------------------------------------------------------------------------------------
#                                                                             data_update
# ---------------------------------------------------------------------------------------
def test_data_update_not_loged(client, jan_2000):
    login_rediretion(
        client,
        'reports:data_update',
        kwargs={**jan_2000, 'pk': 99}
    )


def test_data_update(client, login, post_data, jan_2000):
    obj = DataFactory()
    url = reverse('reports:data_update', kwargs={**jan_2000, 'pk': obj.pk})
    response = client.post(url, data=post_data)

    actual = json.loads(response.content)

    content = actual['html_list']

    assert actual['form_is_valid']
    assert '<td class="text-center">10.12</td>' in content  # distance
    assert '<td class="text-center">0:00:15</td>' in content  # time
    assert '<td class="text-center">1.1</td>' in content  # temperature
    assert '<td class="text-center">600</td>' in content  # ascent
    assert '<td class="text-center">500</td>' in content  # descent
    assert '<td class="text-center">110.0</td>' in content  # max_speed
    assert '<td class="text-center">120</td>' in content  # cadence
    assert '<td class="text-center">200</td>' in content  # heart rate

    row = ('<tr id="row_id_{id}" data-pk="{id}" data-url="{url}" data-tbl="0" class="">')
    assert row.format(id=obj.pk, url=url) in content  # row checked


def test_data_update_loaded_form(client, login, jan_2000):
    obj = DataFactory()
    url = reverse('reports:data_update', kwargs={**jan_2000, 'pk': obj.pk})
    response = client.get(url)

    actual = json.loads(response.content)
    content = actual['html_form']

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
    assert '<input type="hidden" name="checked" value="n"' in content


def test_data_update_object_not_found(client, login, jan_2000):
    url = reverse('reports:data_update', kwargs={**jan_2000, 'pk': 99})
    response = client.get(url)

    assert response.status_code == 404


# ---------------------------------------------------------------------------------------
#                                                                       data_quick_update
# ---------------------------------------------------------------------------------------
def test_data_quick_update_not_loged(client, jan_2000):
    login_rediretion(client, 'reports:data_quick_update', kwargs={**jan_2000, 'pk': 99})


def test_data_quick_update(client, login, jan_2000):
    obj = DataFactory()

    assert obj.checked == 'n'

    url_quick_update = reverse(
        'reports:data_quick_update',
        kwargs={**jan_2000, 'pk': obj.pk}
    )
    url_update = reverse(
        'reports:data_update',
        kwargs={**jan_2000, 'pk': obj.pk}
    )
    response = client.get(url_quick_update)
    actual = json.loads(response.content)

    # empty class="" means checked=y
    row = '<tr id="row_id_{id}" data-pk="{id}" data-url="{url}" data-tbl="0" class="">'
    assert row.format(url=url_update, id=obj.pk) in actual['html_list']


def test_data_quick_update_404(client, login, jan_2000):
    url_quick_update = reverse(
        'reports:data_quick_update',
        kwargs={**jan_2000, 'pk': 99}
    )
    response = client.get(url_quick_update)

    assert response.status_code == 404


def test_data_quick_update_user_items(client_logged, jan_2000):
    obj = DataFactory()
    DataFactory(user=UserFactory(username='xxx'))

    url_quick_update = reverse(
        'reports:data_quick_update',
        kwargs={**jan_2000, 'pk': obj.pk}
    )

    response = client_logged.get(url_quick_update)

    assert len(response.context['objects']) == 1
    assert response.context['objects'][0].user.username == 'bob'
