import calendar
import itertools as it
from dataclasses import dataclass, field
from typing import Union

import polars as pl
from django.db.models import F

from ...data.models import Data
from ...goals.models import Goal

pl.Config.with_columns_kwargs = True


@dataclass
class ProgressData:
    year: int = field(init=True, default=None)
    goal: int = field(init=False, default=0)
    data: list = field(init=False, default_factory=list)

    def __post_init__(self):
        self.goal = self._get_goal()
        self.data = list(self._get_data())

    def _get_goal(self):
        goal = list(
            Goal.objects.items().filter(year=self.year).values_list("goal", flat=True)
        )
        return goal[0] if goal else 0

    def _get_data(self):
        return Data.objects.items(year=self.year).values(
            "date",
            "distance",
            "time",
            "ascent",
            bikes=F("bike__short_name"),
            temp=F("temperature"),
        )


class Progress:
    def __init__(self, data: ProgressData):
        self._year = data.year
        self._goal = data.goal

        self._df = self._build_df(data.data)

    def extremums(self) -> Union[dict, list[dict]]:
        if self._df.is_empty():
            return []

        _agg = [
            self._agg_min_max(col) for col in ["distance", "temp", "ascent", "speed"]
        ]

        df = (
            self._df.lazy()
            .select(["date", "ascent", "temp", "speed", "distance"])
            .with_columns(pl.col("temp").fill_null(0))
            .with_columns((pl.col("date").dt.year()).alias("year"))
            .group_by("year")
            .agg(list(it.chain.from_iterable(_agg)))
            .sort(pl.col("year"), descending=True)
        )
        return df.collect().to_dicts()

    def season_progress(self) -> list[dict]:
        if not self._year or self._df.is_empty():
            return []

        df = (
            self._df.lazy()
            .sort("date")
            .pipe(self._progress_season)
            .pipe(self._progress_month)
            .pipe(self._progress_goals)
            .pipe(self._progress_dtypes)
            .sort("date", descending=True)
        )
        return df.collect().to_dicts()

    def _progress_season(self, df: pl.DataFrame) -> pl.Expr:
        day_of_year = pl.col("date").dt.ordinal_day()
        return df.with_columns(
            season_distance=pl.col("distance").cum_sum(),
            season_seconds=pl.col("seconds").cum_sum(),
            season_ascent=pl.col("ascent").cum_sum(),
        ).with_columns(
            season_per_day=pl.col("season_distance") / day_of_year,
            season_speed=self._speed("season_distance", "season_seconds"),
        )

    def _progress_month(self, df: pl.DataFrame) -> pl.Expr:
        month = pl.col("date").dt.month()
        speed = self._speed("month_distance", "month_seconds")
        return (
            df.with_columns(
                month=month,
                monthlen=month.map_elements(
                    lambda x: calendar.monthrange(self._year, x)[1],
                    return_dtype=pl.Int8,
                ),
            )
            .with_columns(
                month_seconds=pl.col("seconds").sum().over("month"),
                month_distance=pl.col("distance").sum().over("month"),
                month_ascent=pl.col("ascent").sum().over("month"),
            )
            .with_columns(
                month_speed=speed.over("month"),
                month_per_day=pl.col("month_distance") / pl.col("monthlen"),
            )
        )

    def _progress_goals(self, df: pl.DataFrame) -> pl.Expr:
        day_of_year = pl.col("date").dt.ordinal_day()
        year_len = 366 if calendar.isleap(self._year) else 365
        per_day = self._goal / year_len
        percent = (pl.col("season_distance") * 100) / pl.col("goal_per_day")
        delta = pl.col("season_distance") - pl.col("goal_per_day")
        return df.with_columns(goal_per_day=(day_of_year * per_day)).with_columns(
            goal_percent=percent,
            goal_delta=delta,
        )

    def _progress_dtypes(self, df: pl.DataFrame) -> pl.Expr:
        return df.with_columns(
            [
                pl.col("season_seconds").cast(pl.Int32),
                pl.col("season_speed").cast(pl.Float32),
                pl.col("season_per_day").cast(pl.Float32),
                pl.col("season_ascent").cast(pl.Int32),
                pl.col("goal_per_day").cast(pl.Float32),
                pl.col("goal_percent").cast(pl.Float32),
                pl.col("goal_delta").cast(pl.Float32),
                pl.col("monthlen").cast(pl.Int8),
                pl.col("month").cast(pl.Int8),
                pl.col("month_distance").cast(pl.Float32),
                pl.col("month_seconds").cast(pl.Int32),
                pl.col("month_speed").cast(pl.Float32),
                pl.col("month_per_day").cast(pl.Float32),
                pl.col("month_ascent").cast(pl.Int32),
            ]
        )

    def _build_dtypes(self) -> pl.Expr:
        return [
            pl.col("bikes").cast(pl.Categorical),
            pl.col("distance").cast(pl.Float32),
            pl.col("ascent").cast(pl.Int16),
            pl.col("temp").cast(pl.Float32),
            pl.col("seconds").cast(pl.Int32),
            pl.col("speed").cast(pl.Float32),
        ]

    def _build_df(self, data: list[dict]) -> pl.DataFrame:
        df = pl.DataFrame(data=data)
        if df.is_empty():
            return df

        df = (
            df.lazy()
            .with_columns(pl.col("time").dt.total_seconds().alias("seconds"))
            .with_columns(self._speed("distance", "seconds").alias("speed"))
            .with_columns(self._build_dtypes())
        ).collect()

        return df.drop("time")

    def _speed(self, distance_km: str, time_seconds: str) -> pl.Expr:
        return pl.col(distance_km) / (pl.col(time_seconds) / 3600)

    def _agg_min_max(self, col: str) -> pl.Expr:
        return (
            pl.col(col).sort_by(col).last().alias(f"max_{col}"),
            pl.col("date").sort_by(col).last().alias(f"max_{col}_date"),
            pl.col(col).sort_by(col).first().alias(f"min_{col}"),
            pl.col("date").sort_by(col).first().alias(f"min_{col}_date"),
        )
