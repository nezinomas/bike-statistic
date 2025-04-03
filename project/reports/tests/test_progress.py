from datetime import date, timedelta
from types import SimpleNamespace

import pytest

from ..library.progress import Progress

pytestmark = pytest.mark.django_db


@pytest.fixture(name="data")
def fixture_data():
    data = [
        {
            "date": date(2000, 1, 1),
            "distance": 2,
            "time": timedelta(seconds=2_000),
            "ascent": 2,
            "bikes": "Short Name",
            "temp": 2,
        },
        {
            "date": date(2000, 1, 2),
            "distance": 20,
            "time": timedelta(seconds=2_000),
            "ascent": 200,
            "bikes": "Short Name",
            "temp": 20,
        },
        {
            "date": date(2000, 1, 31),
            "distance": 200,
            "time": timedelta(seconds=2_000),
            "ascent": 2000,
            "bikes": "Short Name",
            "temp": 100,
        },
    ]

    return SimpleNamespace(year=2000, goal=1000, data=data)


@pytest.fixture(name="no_data")
def fixture_no_data():
    return SimpleNamespace(year=2000, goal=0, data=[])


# -------------------------------------------------------------------------------------
#                                                                             extremums
# -------------------------------------------------------------------------------------
def test_extremums_no_data(no_data):
    actual = Progress(no_data).extremums()

    assert actual == []


def test_extremums_distance(data):
    actual = Progress(data).extremums()

    assert actual[0]["max_distance"] == 200.0
    assert actual[0]["max_distance_date"] == date(2000, 1, 31)

    assert actual[0]["min_distance"] == 2.0
    assert actual[0]["min_distance_date"] == date(2000, 1, 1)


def test_extremums_temperature(data):
    data.data.extend(
        [
            {
                "date": date(2000, 3, 1),
                "distance": 2,
                "time": timedelta(seconds=2_000),
                "ascent": 2,
                "bikes": "Short Name",
                "temp": None,
            },
            {
                "date": date(2000, 4, 1),
                "distance": 2,
                "time": timedelta(seconds=2_000),
                "ascent": 2,
                "bikes": "Short Name",
                "temp": -22,
            },
        ]
    )
    actual = Progress(data).extremums()

    assert actual[0]["max_temp_date"] == date(2000, 1, 31)
    assert actual[0]["max_temp"] == 100

    assert actual[0]["min_temp_date"] == date(2000, 4, 1)
    assert actual[0]["min_temp"] == -22


def test_extremums_ascent(data):
    actual = Progress(data).extremums()

    assert actual[0]["max_ascent_date"] == date(2000, 1, 31)
    assert actual[0]["max_ascent"] == 2000


def test_extremums_speed(data):
    actual = Progress(data).extremums()

    assert actual[0]["max_speed_date"] == date(2000, 1, 31)
    assert actual[0]["max_speed"] == 360.0


def test_season_progress_keys(data):
    actual = Progress(data).season_progress()

    assert "date" in actual[0]
    assert "bikes" in actual[0]
    assert "distance" in actual[0]
    assert "temp" in actual[0]
    assert "ascent" in actual[0]
    assert "seconds" in actual[0]
    assert "speed" in actual[0]
    assert "season_distance" in actual[0]
    assert "season_seconds" in actual[0]
    assert "season_ascent" in actual[0]
    assert "season_speed" in actual[0]
    assert "season_per_day" in actual[0]
    assert "goal_per_day" in actual[0]
    assert "goal_percent" in actual[0]
    assert "goal_delta" in actual[0]
    assert "month" in actual[0]
    assert "monthlen" in actual[0]
    assert "month_seconds" in actual[0]
    assert "month_distance" in actual[0]
    assert "month_speed" in actual[0]
    assert "month_per_day" in actual[0]
    assert "month_ascent" in actual[0]


def test_progress_monthlen(data):
    actual = Progress(data).season_progress()

    assert actual[0]["monthlen"] == actual[1]["monthlen"] == actual[2]["monthlen"] == 31


def test_progress_month(data):
    actual = Progress(data).season_progress()

    assert actual[0]["month"] == actual[1]["month"] == actual[2]["month"] == 1


def test_progress_month_seconds(data):
    actual = Progress(data).season_progress()

    assert (
        actual[0]["month_seconds"]
        == actual[1]["month_seconds"]
        == actual[2]["month_seconds"]
        == 6000
    )


def test_progress_month_distance(data):
    actual = Progress(data).season_progress()

    assert (
        actual[0]["month_distance"]
        == actual[1]["month_distance"]
        == actual[2]["month_distance"]
        == 222
    )


def test_progress_month_ascent(data):
    actual = Progress(data).season_progress()

    assert (
        actual[0]["month_ascent"]
        == actual[1]["month_ascent"]
        == actual[2]["month_ascent"]
        == 2202
    )


def test_progress_month_speed(data):
    actual = Progress(data).season_progress()

    assert (
        round(actual[0]["month_speed"], 2)
        == round(actual[1]["month_speed"], 2)
        == round(actual[2]["month_speed"], 2)
        == 133.2
    )


def test_progress_month_per_day(data):
    actual = Progress(data).season_progress()

    assert (
        round(actual[0]["month_per_day"], 2)
        == round(actual[1]["month_per_day"], 2)
        == round(actual[2]["month_per_day"], 2)
        == round(222 / 31, 2)
    )


def test_season_progress_sorting(data):
    actual = Progress(data).season_progress()

    assert date(2000, 1, 31) == actual[0]["date"]
    assert date(2000, 1, 2) == actual[1]["date"]
    assert date(2000, 1, 1) == actual[2]["date"]


def test_season_progress_distance_cumulative_sum(data):
    actual = Progress(data).season_progress()

    assert actual[0]["season_distance"] == 222.0
    assert actual[1]["season_distance"] == 22.0
    assert actual[2]["season_distance"] == 2.0


def test_season_progress_seconds_cumulative_sum(data):
    actual = Progress(data).season_progress()

    assert round(actual[0]["season_seconds"], 2) == 6000
    assert round(actual[1]["season_seconds"], 2) == 4000
    assert round(actual[2]["season_seconds"], 2) == 2000


def test_season_progress_season_speed(data):
    actual = Progress(data).season_progress()

    assert round(actual[0]["season_speed"], 2) == 133.2
    assert round(actual[1]["season_speed"], 2) == 19.8
    assert round(actual[2]["season_speed"], 2) == 3.6


def test_season_progress_goal_percents(data):
    actual = Progress(data).season_progress()

    assert round(actual[0]["goal_percent"], 2) == 262.1
    assert round(actual[1]["goal_percent"], 2) == 402.6
    assert round(actual[2]["goal_percent"], 2) == 73.2


def test_season_progress_day_goal(data):
    actual = Progress(data).season_progress()

    assert round(actual[0]["goal_per_day"], 2) == 84.7
    assert round(actual[1]["goal_per_day"], 2) == 5.46
    assert round(actual[2]["goal_per_day"], 2) == 2.73


def test_season_progress_day_goal_two_months(data):
    data.data = [
        {
            "date": date(2000, 1, 1),
            "distance": 2,
            "time": timedelta(seconds=2_000),
            "ascent": 2,
            "bikes": "Short Name",
            "temp": 2,
        },
        {
            "date": date(2000, 2, 1),
            "distance": 2,
            "time": timedelta(seconds=2_000),
            "ascent": 2,
            "bikes": "Short Name",
            "temp": 2,
        },
    ]
    data.goal = 366
    actual = Progress(data).season_progress()

    assert round(actual[0]["goal_per_day"], 2) == 32
    assert round(actual[1]["goal_per_day"], 2) == 1


def test_season_progress_day_goal_empty(data):
    data.goal = 0
    actual = Progress(data).season_progress()
    assert actual[0]["goal_per_day"] == 0.0
    assert actual[1]["goal_per_day"] == 0.0
    assert actual[2]["goal_per_day"] == 0.0


def test_season_progress_km_delta(data):
    actual = Progress(data).season_progress()

    assert round(actual[0]["goal_delta"], 2) == 137.3
    assert round(actual[1]["goal_delta"], 2) == 16.54
    assert round(actual[2]["goal_delta"], 2) == -0.73


def test_season_progress_per_day_season(data):
    actual = Progress(data).season_progress()

    assert round(actual[0]["season_per_day"], 2) == 7.16
    assert round(actual[1]["season_per_day"], 2) == 11.0
    assert round(actual[2]["season_per_day"], 2) == 2.0


def test_season_progress_ascent_cumulative_sum(data):
    actual = Progress(data).season_progress()

    assert actual[0]["season_ascent"] == 2202
    assert actual[1]["season_ascent"] == 202
    assert actual[2]["season_ascent"] == 2


def test_season_progress_workout_speed(data):
    actual = Progress(data).season_progress()

    assert round(actual[0]["speed"], 2) == 360.0
    assert round(actual[1]["speed"], 2) == 36.0
    assert round(actual[2]["speed"], 2) == 3.6
