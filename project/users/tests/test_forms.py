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

    assert '<input type="text" name="garmin_user"' in form
    assert '<input type="password" name="garmin_password"' in form


def test_external_initial_value(get_user):
    UserFactory()

    form = ExternalUserForm().as_p()

    assert '<input type="text" name="garmin_user" value="ebob"' in form


def test_external_blank_data(get_user):
    form = ExternalUserForm(data={})

    assert not form.is_valid()

    assert len(form.errors) == 2

    assert "garmin_user" in form.errors
    assert "garmin_password" in form.errors


def test_external_valid_data(get_user):
    UserFactory()

    form = ExternalUserForm(
        data={
            "garmin_user": "user@email.com",
            "garmin_password": "123456",
        }
    )

    assert form.is_valid()

    form.save()

    actual = User.objects.all()
    assert actual.count() == 1

    actual = actual[0]

    assert actual.username == "bob"
    assert actual.garmin_user == "user@email.com"
    assert utils.decrypt(actual.garmin_password) == "123456"
