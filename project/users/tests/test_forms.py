import pytest

from ...core.lib import utils
from ...users.factories import UserFactory
from ...users.models import User
from ..forms import ExternalUserForm

pytestmark = pytest.mark.django_db


def test_external_init(get_user):
    ExternalUserForm()


def test_external_fields(get_user):
    form = ExternalUserForm().as_p()

    assert '<input type="text" name="endomondo_user"' in form
    assert '<input type="password" name="endomondo_password"' in form


def test_external_initial_value(get_user):
    UserFactory()

    form = ExternalUserForm().as_p()

    assert '<input type="text" name="endomondo_user" value="ebob"' in form


def test_external_blank_data(get_user):
    form = ExternalUserForm(data={})

    assert not form.is_valid()

    assert len(form.errors) == 2

    assert 'endomondo_user' in form.errors
    assert 'endomondo_password' in form.errors


def test_external_valid_data(get_user):
    UserFactory()

    form = ExternalUserForm(data={
        'endomondo_user': 'user@email.com',
        'endomondo_password': '123456',
    })

    assert form.is_valid()

    form.save()

    actual = User.objects.all()
    assert actual.count() == 1

    actual = actual[0]

    assert actual.username == 'bob'
    assert actual.endomondo_user == 'user@email.com'
    assert utils.decrypt(actual.endomondo_password) == '123456'
