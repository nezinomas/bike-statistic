import pytest
import time_machine

from ..context import years


@time_machine.travel('2001-1-1')
@pytest.mark.django_db
def test_years_in_context(rf, get_user):
    r = rf.get('/fake/')

    actual = years(r)

    assert actual['years'] == [2001, 2000]
