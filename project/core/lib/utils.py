from datetime import datetime
from typing import List

from crequest.middleware import CrequestMiddleware


def get_user():
    request = CrequestMiddleware.get_request()
    return request.user


def years() -> List[int]:
    now = datetime.now().year
    start = now

    try:
        start = get_user().date_joined.year
    except AttributeError:
        pass

    _years = [x for x in range(start, now + 1)]

    return _years
