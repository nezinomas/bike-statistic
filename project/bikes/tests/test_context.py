import pytest

from ...bikes.factories import BikeFactory
from ...users.factories import UserFactory
from ..context import bike_list


@pytest.mark.django_db
def test_bike_list(rf, get_user):
    BikeFactory(short_name='B1')
    BikeFactory(short_name='B2', user=UserFactory(username='xxx'))

    r = rf.get('/fake/')

    actual = bike_list(r)

    assert len(actual['bike_list']) == 1
    assert actual['bike_list'][0].short_name == 'B1'
