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
        'temperature': 0.0,
        'ascent': 0.0,
        'descent': 0.0,
        'max_speed': 0.0,
        'cadence': 0,
        'heart_rate': 0,
        'checked': 'y'
    }
