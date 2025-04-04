import pytest
from django.urls import resolve, reverse

from .. import views
from ..factories import UserFactory

pytestmark = pytest.mark.django_db


def test_custom_login_func():
    view = resolve("/login/")

    assert views.Login == view.func.view_class


def test_custom_logout_func():
    view = resolve("/logout/")

    assert views.Logout == view.func.view_class


def test_logout_redirects_to_login(client_logged):
    url = reverse("users:logout")
    response = client_logged.get(url, follow=True)

    assert response.status_code == 200
    assert response.resolver_match.url_name == "login"


def test_successful_login(client):
    UserFactory()

    url = reverse("users:login")
    credentials = {"username": "bob", "password": "123"}

    response = client.post(url, credentials, follow=True)

    assert response.status_code == 200
    assert response.context["user"].is_authenticated


def test_sync_update():
    view = resolve("/profile/sync/")

    assert views.sync_update is view.func


def test_sync_update_loging_required(client):
    url = reverse("users:sync_update")
    response = client.get(url, follow=True)

    assert response.status_code == 200
    assert response.resolver_match.url_name == "login"


def test_sync_update_200(client_logged):
    url = reverse("users:sync_update")
    response = client_logged.get(url)

    assert response.status_code == 200
