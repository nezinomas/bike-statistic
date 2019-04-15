import pytest
from django.urls import resolve, reverse

from .. import views
from ..factories import UserFactory


pytestmark = pytest.mark.django_db

@pytest.fixture(autouse=True)
def login(client):
    UserFactory()
    client.login(username='bob', password='123')


def test_data_list_valid_date(client):
    url = reverse(
        'reports:data_list',
        kwargs={
            'start_date': '2000-01-01',
            'end_date': '2000-01-31'
        }
    )
    response = client.get(url)

    assert '<form class="filter"' in str(response.content)
    assert 'bob' in str(response.content)

