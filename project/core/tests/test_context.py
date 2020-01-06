import pytest
from freezegun import freeze_time

from ..context import years


@freeze_time('2000-1-1')
@pytest.mark.django_db
def test_years_in_context(rf, get_user):
    r = rf.get('/fake/')

    actual = years(r)

    assert actual['years'] == [2000, 1999]
