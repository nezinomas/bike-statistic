import base64
import contextlib
import logging
import traceback
from datetime import datetime
from typing import List

from crequest.middleware import CrequestMiddleware
from cryptography.fernet import Fernet
from django.conf import settings


def get_user():
    request = CrequestMiddleware.get_request()
    return request.user


def encrypt(txt):
    try:
        txt = str(txt)
        key = settings.env('ENCRYPT_KEY').encode()

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
        key = settings.env('ENCRYPT_KEY').encode()

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
