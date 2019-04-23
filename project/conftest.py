import tempfile

import pytest

from .core.factories import UserFactory


@pytest.fixture(scope="session", autouse=True)
def temp_folder_for_cash(tmpdir_factory):
    with tempfile.TemporaryDirectory() as CASH_ROOT:
        pass


@pytest.fixture()
def login(client, django_db_blocker):
    UserFactory()

    client.login(username='bob', password='123')
