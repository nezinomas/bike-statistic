import pytest
from django.urls import resolve, reverse
from mock import patch
from .. import views


@pytest.mark.django_db
def test_insert_view_status_code_200(client, login):
    url = reverse('reports:insert_data')
    response = client.get(url)

    assert 200 == response.status_code


def test_view_func():
    view = resolve('/data/insert/')

    assert view.func == views.insert_data


@pytest.mark.django_db
def test_insert_data_redirection_if_user_not_logged(client):
        login_url = reverse('accounts:login')
        url = reverse('reports:insert_data')
        response = client.get(url)

        assert response.url == '{login_url}?next={url}'.format(
            login_url=login_url, url=url)


@patch('project.reports.views.data.inserter', return_value=True)
@pytest.mark.django_db
def test_insert_data_no_errors(mocked, client, login):
    url = reverse('reports:insert_data')
    response = client.get(url)

    assert response.url == reverse('reports:data_empty')


@patch('project.reports.views.data.inserter', side_effect=Exception())
@pytest.mark.django_db
def test_insert_data_exception_occurs(mocked, client, login):
    url = reverse('reports:insert_data')
    response = client.get(url)

    assert 'An exception of type Exception occurred.' in str(response.content)
