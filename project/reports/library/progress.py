import calendar
import itertools as it
from dataclasses import dataclass, field

import polars as pl
from django.db.models import F

from ...data.models import Data
from ...goals.models import Goal

pl.Config.with_columns_kwargs = True


@dataclass
class ProgressData:
    year: int
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

    def extremums(self):
        if self._df.is_empty():
            return self._df

        _agg = [
            self._agg_min_max(col) for col in ["distance", "temp", "ascent", "speed"]
        ]

        df = (
            self._df.lazy()
            .select(["date", "ascent", "temp", "speed", "distance"])
            .with_column((pl.col("date").dt.year()).alias("year"))
            .groupby("year")
            .agg(list(it.chain.from_iterable(_agg)))
            .sort(pl.col("year"), reverse=True)
        ).collect()
        dicts = df.to_dicts()
        return dicts[0] if self._year else dicts

    def season_progress(self):
        if self._df.is_empty() or not self._year:
            return self._df

        df = (
            self._df.lazy()
            .sort("date")
            .pipe(self._progress_season)
            .pipe(self._progress_goals)
            .pipe(self._progress_month)
            .with_columns(self._progress_dtypes())
            .sort("date", reverse=True)
        ).collect()
        return df.to_dicts()

    def _progress_season(self, df) -> pl.Expr:
        return df.with_columns(
            season_distance=pl.col("distance").cumsum(),
            season_seconds=pl.col("seconds").cumsum(),
            season_ascent=pl.col("ascent").cumsum(),
        ).with_columns(
            season_per_day=pl.col("season_distance") / pl.col("date").dt.day(),
            season_speed=self._speed("season_distance", "season_seconds"),
        )

    def _progress_month(self, df):
        month = pl.col("date").dt.month()
        speed = self._speed("month_distance", "month_seconds")
        return (
            df.with_columns(
                month=month,
                monthlen=month.apply(lambda x: calendar.monthrange(2000, x)[1]),
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

    def _progress_goals(self, df):
        year_len = 366 if calendar.isleap(self._year) else 365
        per_day = self._goal / year_len
        percent = (pl.col("season_distance") * 100) / pl.col("goal_day")
        return (df
            .with_columns(
                goal_day=pl.col("date").dt.day() * per_day)
            .with_columns(
                goal_percent=percent,
                goal_delta=pl.col("season_distance") - pl.col("goal_day")))

    def _progress_dtypes(self) -> pl.Expr:
        return [
            pl.col("season_seconds").cast(pl.Int32),
            pl.col("season_speed").cast(pl.Float32),
            pl.col("season_per_day").cast(pl.Float32),
            pl.col("season_ascent").cast(pl.Int32),
            pl.col("goal_day").cast(pl.Float32),
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

    def _build_dtypes(self) -> pl.Expr:
        return [
            pl.col("bikes").cast(pl.Categorical),
            pl.col("distance").cast(pl.Float32),
            pl.col("ascent").cast(pl.Int16),
            pl.col("temp").cast(pl.Float32),
            pl.col("seconds").cast(pl.Int32),
            pl.col("speed").cast(pl.Float32),
        ]

    def _build_df(self, data):
        df = pl.DataFrame(data=data)
        if df.is_empty():
            return df

        df = (
            df.lazy()
            .with_columns([pl.col("time").dt.seconds().alias("seconds")])
            .with_columns([self._speed("distance", "seconds").alias("speed")])
            .with_columns(self._build_dtypes())
        ).collect()

        df = df.drop("time")
        return df

    def _speed(self, distance_km, time_seconds):
        return pl.col(distance_km) / (pl.col(time_seconds) / 3600)

    def _agg_min_max(self, col: str) -> pl.Expr:
        return (
            pl.col(col).sort_by(col).last().alias(f"max_{col}"),
            pl.col("date").sort_by(col).last().alias(f"max_{col}_date"),
            pl.col(col).sort_by(col).first().alias(f"min_{col}"),
            pl.col("date").sort_by(col).first().alias(f"min_{col}_date"),
        )
