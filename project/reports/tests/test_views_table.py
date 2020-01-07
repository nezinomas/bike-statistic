import pytest
from django.urls import resolve, reverse

from ...core.helpers.test_helpers import login_rediretion
from ...goals.factories import GoalFactory
from .. import views


def test_view_table_not_loged(client):
    login_rediretion(client, 'reports:reports_table', kwargs={'year': 2000})


@pytest.mark.django_db
def test_view_table_200(client, login):
    GoalFactory()

    url = reverse('reports:reports_table', kwargs={'year': 2000})
    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_view_table_404(client, login):
    url = reverse('reports:reports_table', kwargs={'year': 2000})
    response = client.get(url)

    assert response.status_code == 404


def test_view_table_func():
    view = resolve('/reports/2000/')

    assert view.func == views.table


@pytest.mark.django_db
def test_view_table_template(client, login):
    GoalFactory()

    url = reverse('reports:reports_table', kwargs={'year': 2000})
    response = client.get(url)

    assert response.templates[0].name == 'reports/table.html'


@pytest.mark.django_db
def test_view_table_context_has_items(client, login):
    GoalFactory()

    url = reverse('reports:reports_table', kwargs={'year': 2000})
    response = client.get(url)

    assert 'objects' in response.context
    assert 'month' in response.context
    assert 'year' in response.context
    assert 'stats' in response.context
