import json

import pytest
from django.urls import resolve, reverse
from freezegun import freeze_time

from ...core.factories import DataFactory
from ...core.helpers.test_helpers import login_rediretion
from .. import forms
from ..models import Data
from ..views import data, data_list


def last_id():
    return Data.objects.values_list('id', flat=True)[0]


def test_data_list_not_loged(client):
    login_rediretion(
        client,
        'reports:data_list',
        kwargs={'start_date': '2000-01-01', 'end_date': '2000-01-31'}
    )


@pytest.mark.django_db
def test_data_list_valid_date(client, login):
    url = reverse(
        'reports:data_list',
        kwargs={
            'start_date': '2000-01-01',
            'end_date': '2000-01-31'
        }
    )
    response = client.get(url)

    assert '<form class="filter"' in str(response.content)
    assert 'bob' in str(response.content)


def test_data_list_not_valid_date_01(client):
        response = client.get('/data/2000/2001/')
        assert 404 == response.status_code


def test_data_list_not_valid_date_02(client):
    response = client.get('/data/xxxx-xx-xx/xxxx-xx-xx/')
    assert 404 == response.status_code


@pytest.mark.django_db
def test_data_list_date_filter_redirection(client, login):
    url = reverse(
        'reports:data_list',
        kwargs={
            'start_date': '1999-01-01',
            'end_date': '1999-01-01'
        }
    )
    data = {
        'date_filter': True,
        'start_date': '2000-01-01',
        'end_date': '2000-01-31'
    }
    response = client.post(url, data=data, follow=True)

    assert 200 == response.status_code
    assert data_list == resolve(response.redirect_chain[0][0]).func

    assert (
        '<input type="text" name="start_date" value="2000-01-01"'
        in str(response.content)
    )
    assert (
        '<input type="text" name="end_date" value="2000-01-31"'
        in str(response.content)
    )


@pytest.mark.django_db
@freeze_time("1999-01-15")
def test_data_partial_redirection(client, login):
    response = client.get('/data/1999-01-01/', follow=True)

    assert 200 == response.status_code
    assert 'data_list' == response.resolver_match.url_name


@freeze_time("1999-01-15")
def test_data_partial_func(client):
    view = resolve('/data/1999-01-01/')
    assert data.data_partial == view.func


@freeze_time("1999-01-15")
@pytest.mark.django_db
def test_data_empty_redirection(client, login):
    response = client.get('/data/', follow=True)

    assert 200 == response.status_code
    assert 'data_list' == response.resolver_match.url_name


@freeze_time("1999-01-15")
def test_data_empty_func(client):
    view = resolve('/data/')
    assert data.data_empty == view.func


@freeze_time("1999-01-15")
@pytest.mark.django_db
def test_index_redirection(client, login):
    response = client.get('/', follow=True)

    assert 200 == response.status_code
    assert 'data_list' == response.resolver_match.url_name


@freeze_time("1999-01-15")
def test_index_func(client):
    view = resolve('/')
    assert data.index == view.func


@pytest.mark.django_db
def test_data_create_form_valid(client, login, post_data):
    url = reverse(
        'reports:data_create',
        kwargs={
            'start_date': '2000-01-01',
            'end_date': '2000-01-31'
        }
    )
    response = client.post(url, data=post_data)
    actual = json.loads(response.content)

    assert actual['form_is_valid']

    assert '<td class="text-center">2000-01-01' in actual['html_list']
    assert '<td class="text-center">10.12</td>' in actual['html_list']
    assert '<td class="text-center">0:00:15</td>' in actual['html_list']

    id = last_id()
    row = '<tr id="row_id_{0}" data-pk="{0}"'
    update = 'data-url="/api/data/2000-01-01/2000-01-31/update/{0}/"'
    delete = 'data-url="/api/data/2000-01-01/2000-01-31/delete/{0}/"'

    assert row.format(id) in actual['html_list']
    assert update.format(id) in actual['html_list']
    assert delete.format(id) in actual['html_list']


@pytest.mark.django_db
def test_data_create_form_invalid(client, login):
    url = reverse(
        'reports:data_create',
        kwargs={
            'start_date': '2000-01-01',
            'end_date': '2000-01-31'
        }
    )
    response = client.post(url, data={})
    actual = json.loads(response.content)

    assert not actual['form_is_valid']


@pytest.mark.django_db
def test_data_delete(client, login):
    data = DataFactory()

    url = reverse(
        'reports:data_delete',
        kwargs={
            'start_date': '2000-01-01',
            'end_date': '2000-01-31',
            'pk': data.pk
        }
    )
    response = client.post(url)

    actual = json.loads(response.content)

    assert actual['form_is_valid']
    assert not Data.objects.all()


@pytest.mark.django_db
def test_data_delete_404(client, login):
    url = reverse(
        'reports:data_delete',
        kwargs={
            'start_date': '2000-01-01',
            'end_date': '2000-01-31',
            'pk': 100
        }
    )
    response = client.post(url)

    assert 404 == response.status_code


@pytest.mark.django_db
def test_data_delete_load_confirm_form(client, login):
    data = DataFactory()

    url = reverse(
        'reports:data_delete',
        kwargs={
            'start_date': '2000-01-01',
            'end_date': '2000-01-31',
            'pk': data.pk
        }
    )
    response = client.get(url)

    actual = json.loads(response.content)

    url = '<form method="post" action="{u}"'.format(u=url)
    msg = (
        'Are you sure you want to delete record: <strong>2000-01-01</strong>'
        ' / <strong>bike</strong>?')

    assert url in actual['html_form']
    assert msg in actual['html_form']
