import tempfile

import pytest

from .core.factories import UserFactory

pytestmark = pytest.mark.django_db


@pytest.fixture(scope="session", autouse=True)
def temp_folder_for_cash(tmpdir_factory):
    with tempfile.TemporaryDirectory() as CASH_ROOT:
        pass


@pytest.fixture(scope='session')
def login(client):
    UserFactory()
    client.login(username='bob', password='123')
