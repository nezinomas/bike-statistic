import calendar
from dataclasses import dataclass, field

import polars as pl
from django.db.models import F

from ...data.models import Data
from ...goals.models import Goal


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
            Goal.objects
            .items()
            .filter(year=self.year)
            .values_list('goal', flat=True)
        )
        return goal[0] if goal else 0

    def _get_data(self):
        return (
            Data.objects
            .items(year=self.year)
            .values(
                'date',
                'distance',
                'time',
                'ascent',
                bikes=F('bike__short_name'),
                temp=F('temperature'),
            ))


class Progress():
    def __init__(self, data: ProgressData):
        self._year = data.year
        self._goal = data.goal

        self._df = self._build_df(data.data)

    def _build_df(self, data):
        df = pl.DataFrame(data)
        if df.is_empty():
            return df

        df = df.with_columns([
                pl.col('time').dt.seconds().alias('seconds'),
            ]).with_columns(
                self._speed('distance', 'seconds').alias('speed')
        )
        df = df.drop('time')
        return df

    def extremums(self):
        if self._df.is_empty():
            return {}

        df = (
            self._df
            .select(['date', 'ascent', 'temp', 'speed', 'distance'])
            .with_column((pl.col('date').dt.year()).alias("year"))
            .groupby('year')
            .agg([
                pl.col('distance').sort_by('distance').last().alias('max_distance'),
                pl.col('date').sort_by('distance').last().alias('max_distance_date'),
                pl.col('distance').sort_by('distance').first().alias('min_distance'),
                pl.col('date').sort_by('distance').first().alias('min_distance_date'),
                pl.col('temp').sort_by('temp').last().alias('max_temp'),
                pl.col('date').sort_by('temp').last().alias('max_temp_date'),
                pl.col('temp').sort_by('temp').first().alias('min_temp'),
                pl.col('date').sort_by('temp').first().alias('min_temp_date'),
                pl.col('ascent').sort_by('ascent').last().alias('max_ascent'),
                pl.col('date').sort_by('ascent').last().alias('max_ascent_date'),
                pl.col('speed').sort_by('speed').last().alias('max_speed'),
                pl.col('date').sort_by('speed').last().alias('max_speed_date'),
            ])
            .sort(pl.col('year'), reverse=True)
        )
        dicts = df.to_dicts()

        return dicts[0] if self._year else dicts


    def _speed(self, distance_km, time_seconds):
        return pl.col(distance_km) / (pl.col(time_seconds) / 3600)

    def season_progress(self):
        df = self._df

        if df.is_empty() or not self._year:
            return {}

        year_len = 366 if calendar.isleap(self._year) else 365
        per_day = self._goal / year_len

        df = (
            df.lazy()
            .sort("date")
            .with_columns([
                pl.col('distance').cumsum().alias('season_distance'),
                pl.col('seconds').cumsum().alias('season_seconds'),
                pl.col('ascent').cumsum().alias('season_ascent'),
            ])
            .with_columns([
                (pl.col('season_distance') / pl.col('date').dt.day()).alias('season_per_day'),
                self._speed('season_distance', 'season_seconds').alias('season_speed'),
            ])
            .with_column(
                (pl.col('date').dt.day() * per_day).alias('goal_day')
            )
            .with_columns([
                ((pl.col('season_distance') * 100) / pl.col('goal_day')).alias('goal_percent'),
                (pl.col('season_distance') - pl.col('goal_day')).alias('goal_delta'),
            ])
            .with_columns([
                pl.col('date').dt.month().apply(
                    lambda x: calendar.monthrange(2000, x)[1]).alias('monthlen'),
                pl.col('date').dt.month().alias('month'),
            ])
            .with_columns([
                pl.col('seconds').sum().over('month').alias('month_seconds'),
                pl.col('distance').sum().over('month').alias('month_distance'),
                pl.col('ascent').sum().over('month').alias('month_ascent'),
            ])
            .with_columns([
                self._speed('month_distance', 'month_seconds').over('month').alias('month_speed'),
                (pl.col('month_distance') / pl.col('monthlen')).alias('month_per_day')
            ])
            .sort("date", reverse=True)
        ).collect()
        return df.to_dicts()
