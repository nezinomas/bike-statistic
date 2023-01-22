import pytest
from django.urls import resolve, reverse

from ...core.helpers.test_helpers import login_rediretion
from .. import views
from ..factories import DataFactory


def test_view_table_not_loged(client):
    login_rediretion(client, 'reports:year_progress', kwargs={'year': 2000})


@pytest.mark.django_db
def test_view_table_200(client, login):
    url = reverse('reports:year_progress', kwargs={'year': 2000})
    response = client.get(url)

    assert response.status_code == 200


def test_view_table_func():
    view = resolve('/data/2000/')

    assert view.func == views.table


@pytest.mark.django_db
def test_view_table_no_records_top_table(client, login):
    url = reverse('reports:year_progress', kwargs={'year': 2000})
    response = client.get(url)

    assert '<td class="bg-warning text-center" colspan="10">No records</td>' in str(
        response.content)


@pytest.mark.django_db
def test_view_table_no_records(client, login):
    url = reverse('reports:year_progress', kwargs={'year': 2000})
    response = client.get(url)

    assert '<td class="bg-warning text-center" colspan="20">No records</td>' in str(
        response.content)


@pytest.mark.django_db
def test_view_table_template(client, login):
    url = reverse('reports:year_progress', kwargs={'year': 2000})
    response = client.get(url)

    assert response.templates[0].name == 'reports/table.html'


@pytest.mark.django_db
def test_view_table_context_has_items(client, login):
    url = reverse('reports:year_progress', kwargs={'year': 2000})
    response = client.get(url)

    assert 'season' in response.context
    assert 'month' in response.context
    assert 'year' in response.context
    assert 'e' in response.context


@pytest.mark.django_db
def test_view_table_queries(get_user, client, login, django_assert_num_queries):
    DataFactory()

    with django_assert_num_queries(5):
        url = reverse('reports:year_progress', kwargs={'year': 2000})
        client.get(url)
