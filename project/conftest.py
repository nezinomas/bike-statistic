import tempfile
from mock import patch
import pytest

from .core.factories import UserFactory


@pytest.fixture()
def login(client, django_db_blocker):
    UserFactory()

    client.login(username='bob', password='123')
