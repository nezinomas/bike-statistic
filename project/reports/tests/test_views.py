import pytest
from django.urls import resolve, reverse

from ...data.factories import DataFactory
from ...users.views import Login
from .. import views

pytestmark = pytest.mark.django_db


def test_year_progress_302(client):
    url = reverse('reports:year_progress', kwargs={'year': 2000})
    response = client.get(url, follow=True)

    assert response.resolver_match.func.view_class is Login


def test_year_progress_200(client_logged):
    url = reverse('reports:year_progress', kwargs={'year': 2000})
    response = client_logged.get(url)

    assert response.status_code == 200


def test_year_progress_func():
    view = resolve('/reports/2000/')

    assert view.func.view_class is views.YearProgress


def test_year_progress_no_records_top_table(client_logged):
    url = reverse('reports:year_progress', kwargs={'year': 2000})
    response = client_logged.get(url)

    assert '<div class="alert alert-warning">No data</div>' in str(
        response.content)


def test_year_progress_no_records(client_logged):
    url = reverse('reports:year_progress', kwargs={'year': 2000})
    response = client_logged.get(url)

    assert '<div class="alert alert-warning">No data</div>' in str(
        response.content)


def test_year_progress_template(client_logged):
    url = reverse('reports:year_progress', kwargs={'year': 2000})
    response = client_logged.get(url)

    assert response.templates[0].name == 'reports/year_progress.html'


def test_year_progress_context_has_items(client_logged):
    url = reverse('reports:year_progress', kwargs={'year': 2000})
    response = client_logged.get(url)

    assert 'year' in response.context
    assert 'extremums' in response.context
    assert 'object_list' in response.context


def test_year_progress_queries(client_logged, django_assert_num_queries):
    DataFactory()

    with django_assert_num_queries(5):
        url = reverse('reports:year_progress', kwargs={'year': 2000})
        client_logged.get(url)


def test_extremums_func():
    view = resolve('/reports/extremums/')
    assert view.func.view_class is views.Extremums


def test_extremums_200(client_logged):
    url = reverse('reports:extremums')
    response = client_logged.get(url)
    assert response.status_code == 200
