from datetime import date

import pytest
from freezegun import freeze_time
from mock import patch

from ..lib import utils


@freeze_time("2001-01-01")
@pytest.mark.django_db
def test_years_user_logged(get_user):
    get_user.date_joined = date(1999, 1, 1)

    actual = utils.years()

    assert actual == [1999, 2000, 2001]


@patch('project.core.lib.utils.get_secret')
def test_encrypt_decrypt(_mock):
    _mock.return_value = "YodhMSc34G6kF-HKTGTwuUapn0IkbPr080Hh3a7tW8k="

    txt = 'abc123'

    encrypted = utils.encrypt(txt)
    decrypted = utils.decrypt(encrypted)

    assert decrypted == txt
