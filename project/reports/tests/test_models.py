import pytest

from ...users.factories import UserFactory
from ..factories import DataFactory
from ..models import Data

pytestmark = pytest.mark.django_db

# ---------------------------------------------------------------------------------------
#                                                                                    Data
# ---------------------------------------------------------------------------------------
def test_data_str():
    obj = DataFactory.build()

    assert str(obj) == '2000-01-01 Short Name'


def test_data_related_qs_count(get_user, django_assert_max_num_queries):
    DataFactory()
    DataFactory()

    assert Data.objects.all().count() == 2

    with django_assert_max_num_queries(1):
        list(q.user.username for q in Data.objects.related())


def test_data_items(get_user):
    DataFactory()

    assert Data.objects.items().count() == 1


def test_data_items_for_logged_user(get_user):
    DataFactory()
    DataFactory(user=UserFactory(username='XXX'))

    assert Data.objects.all().count() == 2
    assert Data.objects.items().count() == 1
