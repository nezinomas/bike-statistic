import pytest
from django.contrib.auth.models import AnonymousUser

from .users.factories import UserFactory


@pytest.fixture(scope="session")
def user(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        u = UserFactory()
    yield u
    with django_db_blocker.unblock():
        u.delete()


@pytest.fixture()
def get_user(monkeypatch):
    user = UserFactory()

    mock_func = "project.core.lib.utils.get_user"
    monkeypatch.setattr(mock_func, lambda: user)

    return user


@pytest.fixture()
def anonymous_user(monkeypatch):
    user_ = AnonymousUser()

    mock_func = "project.core.lib.utils.get_user"
    monkeypatch.setattr(mock_func, lambda: user_)

    return user_


@pytest.fixture()
def client_logged(client):
    UserFactory()
    client.login(username="bob", password="123")

    return client


@pytest.fixture()
def encrypt_key():
    return "YodhMSc34G6kF-HKTGTwuUapn0IkbPr080Hh3a7tW8k="
