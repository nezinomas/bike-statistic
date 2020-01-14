import pytest

from ...core.lib import utils
from ..factories import UserFactory
from ..models import User


def test_user_str():
    actual = UserFactory.build()

    assert str(actual) == 'bob'


@pytest.mark.django_db
def test_user_endomondo_password(encrypt_key):
    u = UserFactory()

    actual = User.objects.get(pk=u.pk)
    actual = utils.decrypt(actual.endomondo_password)

    assert actual == '123'
