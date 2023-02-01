import base64
import contextlib
import logging
import traceback
from datetime import date, datetime
from typing import List, Optional

from crequest.middleware import CrequestMiddleware
from cryptography.fernet import Fernet
from django.conf import settings
from django.utils.timezone import make_aware


def date_to_datetime(
        dt: date,
        hour: Optional[int] = 0,
        minute: Optional[int] = 0,
        second: Optional[int] = 0) -> datetime:

    if isinstance(dt, str):
        year = int(dt[:4])
        month = int(dt[5:7])
        day = int(dt[8:])

    if isinstance(dt, date):
        year = dt.year
        month = dt.month
        day = dt.day

    date_ = datetime(year, month, day, hour, minute, second)
    return make_aware(date_)


def get_user():
    request = CrequestMiddleware.get_request()
    return request.user


def encrypt(txt):
    try:
        txt = str(txt)
        key = settings.ENV('ENCRYPT_KEY').encode()

        cipher_suite = Fernet(key)  # key should be byte
        # input should be byte, so convert the text to byte
        encrypted_text = cipher_suite.encrypt(txt.encode('ascii'))
        # encode to urlsafe base64 format
        encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode("ascii")
        return encrypted_text
    except Exception:
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


def decrypt(txt):
    try:
        key = settings.ENV('ENCRYPT_KEY').encode()

        # base64 decode
        txt = base64.urlsafe_b64decode(txt)
        cipher_suite = Fernet(key)
        return cipher_suite.decrypt(txt).decode("ascii")
    except Exception:
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


def years() -> List[int]:
    now = datetime.now().year
    start = now

    with contextlib.suppress(AttributeError):
        start = get_user().date_joined.year

    return list(range(start, now + 1))


def clean_year_picker_input(field_name, data, cleaned_data, errors):
    # ugly workaround for YearPickerInput field
    # widget returns YYYY-01-01 instead YYYY
    # is it possible to change backend_date_format?
    field = data.get(field_name)
    if not field:
        return cleaned_data
    # try split field by '-'
    try:
        field, *other = field.split('-')
    except AttributeError:
        return cleaned_data
    # try convert field to int
    try:
        int(field)
    except ValueError:
        return cleaned_data
    # if field is in past
    if int(field) < 1974:
        return cleaned_data
    # if error for field exists in errors
    if errors.get(field_name):
        cleaned_data[field_name] = field
        errors.pop(field_name)

    return cleaned_data
