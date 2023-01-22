import pytest

from ..factories import UserFactory
from ..models import User


def test_user_str():
    actual = UserFactory.build()

    assert str(actual) == 'bob'


@pytest.mark.django_db
def test_user_garmin_password(encrypt_key):
    u = UserFactory(username='xxx')

    actual = User.objects.get(pk=u.pk)
    actual = actual.garmin_password

    assert actual == '123'
