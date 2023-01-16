import pytest
from mock import PropertyMock, patch

from ...bikes.factories import BikeFactory
from ...users.factories import UserFactory
from ..library.insert_garmin import SyncWithGarmin as Sync

pytestmark = pytest.mark.django_db


@patch('project.data.library.insert_garmin.Temperature.temperature', new_callable=PropertyMock)
def test_get_bike_with_main(mck, get_user):
    u = UserFactory()
    BikeFactory(main=True, full_name='X')

    actual = Sync()._get_bike(u)

    assert actual.full_name == 'X'


@patch('project.data.library.insert_garmin.Temperature.temperature', new_callable=PropertyMock)
def test_get_bike_no_main(mck, get_user):
    u = UserFactory()
    BikeFactory(full_name='ZZZ', short_name='zzz')
    BikeFactory(full_name='XXX', short_name='xxx')

    actual = Sync()._get_bike(u)

    assert actual.full_name == 'ZZZ'
