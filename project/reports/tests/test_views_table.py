import pytest
from django.urls import resolve, reverse

from .. import views
from ...goals.factories import GoalFactory


@pytest.mark.django_db
def test_view_table_200(client, login):
    GoalFactory()

    url = reverse('reports:reports_table', kwargs={'year': 2000})
    response = client.get(url)

    assert 200 == response.status_code


@pytest.mark.django_db
def test_view_table_404(client, login):
    url = reverse('reports:reports_table', kwargs={'year': 2000})
    response = client.get(url)

    assert 404 == response.status_code


def test_view_table_func():
    view = resolve('/reports/2000/')

    assert view.func == views.table


@pytest.mark.django_db
def test_view_table_template(client, login):
    GoalFactory()

    url = reverse('reports:reports_table', kwargs={'year': 2000})
    response = client.get(url)

    assert 'reports/table.html' == response.templates[0].name
