import pytest

from ...users.factories import UserFactory
from ..factories import GoalFactory
from ..models import Goal

pytestmark = pytest.mark.django_db


# ---------------------------------------------------------------------------------------
#                                                                                    Goal
# ---------------------------------------------------------------------------------------
def test_goal_str():
    obj = GoalFactory.build()

    assert str(obj) == '2000'


def test_goal_related_qs_count(get_user, django_assert_max_num_queries):
    GoalFactory(year=2000)
    GoalFactory(year=2001)

    assert Goal.objects.all().count() == 2

    with django_assert_max_num_queries(1):
        list(q.user.username for q in Goal.objects.related())


def test_goal_items(get_user):
    GoalFactory()

    assert Goal.objects.items().count() == 1


def test_goal_items_for_logged_user(get_user):
    GoalFactory()
    GoalFactory(user=UserFactory(username='XXX'))

    assert Goal.objects.all().count() == 2
    assert Goal.objects.items().count() == 1


@pytest.mark.xfail
def test_goal_unique_for_one_user(get_user):
    _user = UserFactory(username='XXX')

    Goal.objects.create(user=_user, year=2000, goal=1000)
    Goal.objects.create(user=_user, year=2000, goal=1000)


def test_goal_unique_for_two_users(get_user):
    GoalFactory()
    GoalFactory(user=UserFactory(username='XXX'))
