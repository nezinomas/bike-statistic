from calendar import monthrange
from datetime import date, datetime

import pytest
from django.urls import resolve, reverse
from mock import patch

from ...core.helpers.test_helpers import login_rediretion
from .. import views


def current_month_range():
    year = datetime.now().year
    month = datetime.now().month

    return (
        date(year, month, 1),
        date(year, month, monthrange(year, month)[1])
    )


@patch('project.reports.views.data.SyncWithGarmin.insert_data_current_user', return_value=True)
@pytest.mark.django_db
def test_insert_view_status_code_200(mocked, client, login):
    url = reverse('reports:insert_data')
    response = client.get(url, follow=True)

    assert 200 == response.status_code

    start_date, end_date = current_month_range()
    assert response.redirect_chain[1][0] == reverse(
        'reports:data_list',
        kwargs={'start_date': start_date, 'end_date': end_date}
    )


def test_view_func():
    view = resolve('/data/insert/')

    assert view.func == views.insert_data


@pytest.mark.django_db
def test_insert_data_redirection_if_user_not_logged(client):
    login_rediretion(client, 'reports:insert_data')


@patch('project.reports.views.data.SyncWithGarmin.insert_data_current_user', return_value=True)
@pytest.mark.django_db
def test_insert_data_no_errors(mocked, client, login):
    url = reverse('reports:insert_data')
    response = client.get(url)

    assert response.url == reverse('reports:data_empty')


@patch('project.reports.views.data.SyncWithGarmin.insert_data_current_user', side_effect=Exception('Error X'))
@pytest.mark.django_db
def test_insert_data_exception_occurs(mocked, client, login):
    url = reverse('reports:insert_data')
    response = client.get(url)

    assert '<p>Error X</p>' in str(response.content)
    assert '<p>Type: Exception</p>' in str(response.content)
