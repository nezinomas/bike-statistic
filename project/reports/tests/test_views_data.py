import pytest
from django.urls import resolve, reverse
from freezegun import freeze_time

from ..views import data
from ...core.factories import UserFactory


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
