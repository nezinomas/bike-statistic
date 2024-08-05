from calendar import monthrange
from datetime import date, datetime

import pytest
from django.urls import resolve, reverse
from mock import patch

from ...data.views import DataInsert, DataList
from ...users.views import Login
from .. import views


def current_month_range():
    year = datetime.now().year
    month = datetime.now().month

    return (
        date(year, month, 1),
        date(year, month, monthrange(year, month)[1])
    )


@patch('project.data.views.SyncWithGarmin.insert_data_current_user', return_value=True)
@pytest.mark.django_db
def test_insert_view_status_code_200(mocked, client_logged):
    url = reverse('data:data_insert')
    response = client_logged.get(url, follow=True)

    assert 200 == response.status_code

    assert response.resolver_match.func.view_class is DataInsert


def test_view_func():
    view = resolve('/data/insert/')

    assert view.func.view_class is views.DataInsert


@pytest.mark.django_db
def test_insert_data_redirection_if_user_not_logged(client):
    url = reverse('data:data_insert')
    response = client.get(url, follow=True)

    assert response.resolver_match.func.view_class is Login


@patch('project.data.views.SyncWithGarmin.insert_data_current_user', side_effect=Exception('Error X'))
@pytest.mark.django_db
def test_insert_data_exception_occurs(mocked, client_logged):
    url = reverse('data:data_insert')
    response = client_logged.get(url)

    assert '<p>Error X</p>' in str(response.content)
    assert '<p>Type: Exception</p>' in str(response.content)
