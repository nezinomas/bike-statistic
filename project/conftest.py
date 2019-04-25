import tempfile
from mock import patch
import pytest

from .core.factories import UserFactory


@pytest.fixture()
def login(client, django_db_blocker):
    UserFactory()

    client.login(username='bob', password='123')


@pytest.fixture()
def jan_2000():
    return {
        'start_date': '2000-01-01',
        'end_date': '2000-01-31'
    }
