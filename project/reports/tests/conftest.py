from datetime import date, timedelta

import pytest

from ...core.factories import BikeFactory


@pytest.fixture()
def post_data():
    bike = BikeFactory()
    return {
        'bike': str(bike.id),
        'date': date(2000, 1, 1),
        'distance': 10.12,
        'time': timedelta(seconds=15),
        'temperature': 1.1,
        'ascent': 600,
        'descent': 500,
        'max_speed': 110,
        'cadence': 120,
        'heart_rate': 200,
        'checked': 'n'
    }
