import re

import pytest
from django.urls import resolve, reverse

from ...core.lib.tests_utils import clean_content
from ...users.factories import UserFactory
from ...users.views import CustomLogin
from .. import models, views
from ..factories import GoalFactory

pytestmark = pytest.mark.django_db


def test_goal_list_func():
    view = resolve('/goals/')

    assert views.GoalList == view.func.view_class


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

    row_id = f'row-id-{goal.pk}'
    url_update = reverse('goals:goal_update', kwargs={'pk': goal.pk})
    url_delete = reverse('goals:goal_delete', kwargs={'pk': goal.pk})

    # table row
    assert f'<tr id="{row_id}"' in actual
    assert f'hx-target="this" hx-swap="outerHTML" hx-trigger="click[ctrlKey]" hx-get="{url_update}">' in actual
    # edit button
    assert f'<button type="button" class="btn btn-sm btn-warning" hx-get="{url_update}" hx-target="#{row_id}" hx-swap="outerHTML">' in actual
    # delete button
    assert f'<button type="button" class="btn btn-sm btn-danger" hx-get="{url_delete}" hx-target="#dialog" hx-swap="innerHTML">' in actual


def test_goal_create_func():
    view = resolve('/goals/create/')

    assert views.GoalCreate is view.func.view_class


@pytest.mark.freeze_time('2000-2-2')
def test_goal_create_load_form(client_logged):
    url = reverse('goals:goal_create')
    response = client_logged.get(url)
    content = clean_content(response.content)

    assert response.status_code == 200
    assert '<input type="text" name="year" value="2000"' in content


def test_goal_create_save_with_valid_data(client_logged):
    user = UserFactory()

    data = {'year': '2000', 'goal': '666'}

    url = reverse('goals:goal_create')
    client_logged.post(url, data)
    actual = models.Goal.objects.first()

    assert actual.year == 2000
    assert actual.goal == 666
    assert actual.user == user


def test_goal_create_save_form_errors(client_logged):
    data = {}
    url = reverse('goals:goal_create')
    response = client_logged.post(url, data)
    form = response.context['form']
    assert not form.is_valid()
    assert 'year' in form.errors
    assert 'goal' in form.errors


def test_goal_update_func():
    view = resolve('/goals/update/1/')

    assert views.GoalUpdate is view.func.view_class


def test_goal_update_load_form(client_logged):
    goal = GoalFactory()

    url = reverse('goals:goal_update', kwargs={'pk': goal.pk})
    response = client_logged.get(url)
    form = response.context['form'].as_p()

    assert '2000' in form
    assert '1000' in form


def test_goal_update_load_form_close_button(client_logged):
    goal = GoalFactory()

    url = reverse('goals:goal_update', kwargs={'pk': goal.pk})
    response = client_logged.get(url)
    actual = clean_content(response.content)

    url_close = reverse('goals:goal_detail', kwargs={'pk': goal.pk})
    assert f'hx-get="{url_close}"' in actual


def test_goal_update_year(client_logged):
    goal = GoalFactory()

    data = {
        'year': '2002',
        'goal': '1000',
    }

    url = reverse('goals:goal_update', kwargs={'pk': goal.pk})
    client_logged.post(url, data)

    actual = models.Goal.objects.get(pk=goal.pk)

    assert actual.year == 2002
    assert actual.goal == goal.goal


def test_goal_update_goal(client_logged):
    goal = GoalFactory()

    data = {
        'year': '2000',
        'goal': '1001',
    }

    url = reverse('goals:goal_update', kwargs={'pk': goal.pk})
    client_logged.post(url, data)

    actual = models.Goal.objects.get(pk=goal.pk)

    assert actual.year == goal.year
    assert actual.goal == 1001


def test_goal_delete_func():
    view = resolve('/goals/delete/1/')

    assert views.GoalDelete is view.func.view_class


def test_goal_delete_200(client_logged):
    goal = GoalFactory()
    url = reverse('goals:goal_delete', kwargs={'pk': goal.pk})

    response = client_logged.get(url)

    assert response.status_code == 200


def test_goal_delete_load_form(client_logged):
    goal = GoalFactory()
    url = reverse('goals:goal_delete', kwargs={'pk': goal.pk})

    response = client_logged.get(url)
    content = clean_content(response.content)

    res = re.findall(fr'<form.+hx-post="({url})"', content)
    assert res[0] == url
    assert f'<button type="submit" id="_delete" data-pk="{goal.pk}"' in content


def test_goal_delete(client_logged):
    goal = GoalFactory()
    url = reverse('goals:goal_delete', kwargs={'pk': goal.pk})

    client_logged.post(url, {})

    assert models.Goal.objects.all().count() == 0
