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


def test_goal_detail_func():
    view = resolve('/goals/detail/9/')

    assert views.GoalDetail is view.func.view_class


def test_goal_detail(client_logged):
    goal = GoalFactory()

    url = reverse('goals:goal_detail', kwargs={'pk': goal.pk})
    response = client_logged.get(url)

    actual = response.context['object']
    assert response.status_code == 200
    assert actual == goal


def test_goal_detail_links(client_logged):
    goal = GoalFactory()

    url = reverse('goals:goal_detail', kwargs={'pk': goal.pk})
    response = client_logged.get(url)

    actual = clean_content(response.content)
    print(f'------------------------------->\n{actual}\n')
    row_id = f'row-id-{goal.pk}'
    url_update = reverse('goals:goal_update', kwargs={'pk': goal.pk})
    url_delete = reverse('goals:goal_delete', kwargs={'pk': goal.pk})

    # table row
    assert f'<tr id="{row_id}" hx-target="this" hx-swap="outerHTML" hx-trigger="click[ctrlKey]" hx-get="{url_update}">' in actual
    # edit button
    assert f'<button type="button" class="btn btn-sm btn-warning" hx-get="{url_update}" hx-target="#{row_id}" hx-swap="outerHTML">' in actual
    # delete button
    assert f'<button type="button" class="btn btn-sm btn-danger" hx-get="{url_delete}" hx-target="#dialog" hx-swap="innerHTML">' in actual
