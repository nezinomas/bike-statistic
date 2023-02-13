import pytest
import time_machine

from ...users.factories import UserFactory
from ..forms import GoalForm

pytestmark = pytest.mark.django_db


def test_goal_init(get_user):
    GoalForm()


def test_goal_init_fields(get_user):
    form = GoalForm().as_p()

    assert '<input type="text" name="year"' in form
    assert '<input type="number" name="goal"' in form

    assert '<select name="user"' not in form


@time_machine.travel('2001-01-01')
def test_goal_year_initial_value(get_user):
    UserFactory()

    form = GoalForm().as_p()

    assert '<input type="text" name="year" value="2001"' in form


def test_goal_valid_data(get_user):
    form = GoalForm(data={
        'year': '2000',
        'goal': '5000',
    })

    assert form.is_valid()

    data = form.save()

    assert data.year == 2000
    assert data.goal == 5000
    assert data.user.username == 'bob'


def test_goal_blank_data(get_user):
    form = GoalForm(data={})

    assert not form.is_valid()

    assert len(form.errors) == 2
    assert 'year' in form.errors
    assert 'goal' in form.errors
