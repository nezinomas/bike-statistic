import pytest
from django.urls import resolve, reverse

from .. import views

pytestmark = pytest.mark.django_db


# ---------------------------------------------------------------------------------------
#                                                                                    list
# ---------------------------------------------------------------------------------------
def test_goals_list_func():
    view = resolve('/goals/')

    assert views.goals_list == view.func


def test_goals_list_200_no_data(client_logged):
    url = reverse('goals:goals_list')
    response = client_logged.get(url)

    assert response.status_code == 200


def test_goals_list_200(client_logged):
    url = reverse('goals:goals_list')
    response = client_logged.get(url)

    assert response.status_code == 200


def test_goals_list_no_records(client_logged):
    url = reverse('goals:goals_list')
    response = client_logged.get(url)

    assert '<td class="bg-warning text-center" colspan="14">No records</td>' in str(
        response.content)
