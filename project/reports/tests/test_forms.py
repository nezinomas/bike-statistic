import pytest

from ...bikes.factories import BikeFactory
from ...users.factories import UserFactory
from ..forms import DataForm, DateFilterForm


# ---------------------------------------------------------------------------------------
#                                                                             Filter Form
# ---------------------------------------------------------------------------------------
def test_date_filter_form_is_valid(jan_2000):
    form = DateFilterForm(data=jan_2000)

    assert form.is_valid()


def test_date_filter_form_invalid():
    form = DateFilterForm(
        data={
            'start_date': 'xxx',
            'end_date': 'xxx'
        }
    )

    assert not form.is_valid()


def test_date_filter_form_invalid_start_bigger_than_end():
    form = DateFilterForm(
        data={
            'start_date': '2000-01-31',
            'end_date': '2000-01-01'
        }
    )

    assert not form.is_valid()


# ---------------------------------------------------------------------------------------
#                                                                               Data Form
# ---------------------------------------------------------------------------------------
@pytest.mark.django_db
def test_data_form_is_valid(post_data):
    form = DataForm(data=post_data)

    assert form.is_valid()


@pytest.mark.django_db
def test_data_bike_current_user(get_user):
    u = UserFactory(username='xxx')

    BikeFactory(short_name='T1')  # user bob, current user
    BikeFactory(short_name='T2', user=u)  # user xxx

    form = DataForm().as_p()

    assert 'T1' in form
    assert 'T2' not in form
