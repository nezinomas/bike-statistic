from datetime import datetime, timedelta, timezone

import pytest

from ..library.garmin_activity import GarminActivity


@pytest.fixture(name="data")
def fixture_data():
    return {
        "activityName": "Vilnius Road Cycling",
        "startTimeLocal": "2023-01-24 17:41:30",
        "activityType": {
            "typeId": 10,
            "typeKey": "Road_biking",
        },
        "distance": 13357.98046875,
        "duration": 2996.202880859375,
        "elapsedDuration": 3000.2041015625,
        "movingDuration": 2995.0,
        "elevationGain": 130.0,
        "elevationLoss": 134.0,
        "minElevation": 89.19999694824219,
        "maxElevation": 175.1999969482422,
        "averageSpeed": 4.458000183105469,
        "maxSpeed": 10.281999588012695,
        "calories": 404.0,
        "averageHR": 155,
        "maxHR": 185,
        "averageBikingCadenceInRevPerMinute": 91,
        "minTemperature": -6.0,
        "maxTemperature": 22.0,
        "startLatitude": 54.644885156303644,
        "startLongitude": 25.181577187031507,
        "endLatitude": 54.69831802882254,
        "endLongitude": 25.223586950451136,
    }


@pytest.mark.parametrize(
    "activity_type, expect",
    [
        ("cycling", True),
        ("road_biking", True),
        ("biking", True),
        ("commuting", True),
        ("walking", False),
        ("swimming", False),
    ],
)
def test_is_valid_activity(activity_type, expect, data):
    data["activityType"]["typeKey"] = activity_type
    actual = GarminActivity(data)
    assert actual.is_valid_activity == expect


def test_name(data):
    actual = GarminActivity(data)
    assert actual.name == "road_biking"


def test_start_time(data):
    actual = GarminActivity(data)
    assert actual.start_time == datetime(2023, 1, 24, 17, 41, 30, tzinfo=timezone.utc)


def test_distance(data):
    actual = GarminActivity(data)
    assert actual.distance == 13.36


def test_duration(data):
    actual = GarminActivity(data)
    assert actual.duration == timedelta(seconds=2996)


def test_duration_none(data):
    data["duration"] = None
    actual = GarminActivity(data)
    assert actual.duration == timedelta(seconds=0)


def test_max_speed(data):
    actual = GarminActivity(data)
    assert actual.max_speed == 37.02


def test_max_speed_none(data):
    data["maxSpeed"] = None
    actual = GarminActivity(data)
    assert actual.max_speed == 0


def test_ascent(data):
    actual = GarminActivity(data)
    assert actual.ascent == 130


def test_ascent_none(data):
    data["elevationGain"] = None
    actual = GarminActivity(data)
    assert not actual.ascent


def test_descent(data):
    actual = GarminActivity(data)
    assert actual.descent == 134


def test_descent_none(data):
    data["elevationLoss"] = None
    actual = GarminActivity(data)
    assert not actual.descent


def test_avg_hr(data):
    actual = GarminActivity(data)
    assert actual.avg_hr == 155


def test_avg_hr_none(data):
    data["averageHR"] = None
    actual = GarminActivity(data)
    assert not actual.avg_hr


def test_avg_cadence(data):
    actual = GarminActivity(data)
    assert actual.avg_cadence == 91


def test_avg_cadence_none(data):
    data["averageBikingCadenceInRevPerMinute"] = None
    actual = GarminActivity(data)
    assert not actual.avg_cadence


def test_data_object(data):
    actual = GarminActivity(data).data_object
    assert actual["date"] == datetime(2023, 1, 24, 17, 41, 30, tzinfo=timezone.utc)
    assert actual["distance"] == 13.36
    assert actual["time"] == timedelta(seconds=2996)
    assert actual["ascent"] == 130
    assert actual["descent"] == 134
    assert actual["max_speed"] == 37.02
    assert actual["cadence"] == 91
    assert actual["heart_rate"] == 155
