import pytest
from django.urls import resolve, reverse

from ...core.lib.tests_utils import clean_content
from .. import views
from ..factories import GoalFactory
from ...users.views import CustomLogin
pytestmark = pytest.mark.django_db


def test_goal_list_func():
    view = resolve('/goals/')

    assert views.GoalsList == view.func.view_class


def test_goal_list_302(client):
    url = reverse('goals:goal_list')
    response = client.get(url)

    assert response.status_code == 302


def test_goal_list_302_redirect(client):
    url = reverse('goals:goal_list')
    response = client.get(url, follow=True)

    assert response.resolver_match.func.view_class is CustomLogin


def test_goal_list_200(client_logged):
    url = reverse('goals:goal_list')
    response = client_logged.get(url)

    assert response.status_code == 200


def test_goal_list_no_records(client_logged):
    url = reverse('goals:goal_list')
    response = client_logged.get(url)

    assert '<td class="bg-warning text-center" colspan="4">No records</td>' in str(
        response.content)


def test_goal_list(client_logged):
    GoalFactory()

    url = reverse('goals:goal_list')
    response = client_logged.get(url)
    content = clean_content(response.content)

    assert '2000' in content
    assert '1.000' in content
