from calendar import monthrange
from datetime import datetime


def format_date(day: int = None):
    now = datetime.now()
    year = now.year
    month = now.month
    day = day or monthrange(year, month)[1]

    return f'{year}-{month:02d}-{day:02d}'
