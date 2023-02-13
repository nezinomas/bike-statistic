from datetime import datetime, timezone

import pytest
import time_machine

from ..lib import utils


@time_machine.travel("2001-01-01")
@pytest.mark.django_db
def test_years_user_logged(get_user):
    get_user.date_joined = datetime(1999, 1, 1, tzinfo=timezone.utc)

    actual = utils.years()

    assert actual == [1999, 2000, 2001]


def test_encrypt_decrypt(encrypt_key):
    txt = 'abc123'

    encrypted = utils.encrypt(txt)
    decrypted = utils.decrypt(encrypted)

    assert decrypted == txt
