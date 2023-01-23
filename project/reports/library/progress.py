import calendar
from dataclasses import dataclass, field
from datetime import date

import pandas as pd
from django.db.models import F

from ...goals.models import Goal
from ...data.models import Data


@dataclass
class ProgressData:
    year: int
    goal: int = field(init=False, default=0)
    data: list = field(init=False, default_factory=list)

    def __post_init__(self):
        self.goal = self._get_goal()
        self.data = self._get_data()

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
        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)

        df['date'] = pd.to_datetime(df['date'])
        df['distance'] = df['distance'].astype(float)
        df['ascent'] = df['ascent'].astype(int)
        df['time'] = pd.to_timedelta(df['time'], unit='s')
        df['seconds'] = df['time'].dt.total_seconds().astype(int)
        df['speed'] = self._speed(df['distance'], df['seconds'])

        df['year'] = df['date'].dt.year

        return df

    def _speed(self, distance, seconds):
        return distance / (seconds / 3600)

    def _find_extremums(self, df, column):
        functions = {
            'max': df.loc[df[column].idxmax()],
            'min': df.loc[df[column].idxmin()]
        }

        item = {}
        for func_name, row in functions.items():
            if row is not None:
                date_column = f'{column}_{func_name}_date'
                value_column = f'{column}_{func_name}_value'

                item[date_column] = row['date']
                item[value_column] = row[column]

        return item

    def extremums(self):
        df = self._df.copy()

        if df.empty:
            return {}

        columns = [
            'distance',
            'temp',
            'ascent',
            'speed',
        ]

        d = {}
        for column in columns:
            d |= self._find_extremums(df, column)

        return d

    def month_stats(self):
        df = self._df.copy()

        if df.empty:
            return {}

        df.index = df['date']
        df = df.resample('M').sum() # group_by month and get sum of groups

        df['year_month'] = df.index.to_period('M')
        df.loc[:, 'monthlen'] = df.index.day
        df.loc[:, 'distance_per_day'] = df['distance'] / df['monthlen']
        df.loc[:, 'speed'] = self._speed(df['distance'], df['seconds'])

        # make df index year_month
        df.reset_index()
        df.index = df['year_month']
        df.index = df.index.astype(str)

        return df.to_dict('index')

    def season_progress(self):
        df = self._df.copy()
        if df.empty or not self._year:
            return {}
        df = df.sort_values(by='date', ascending=False)

        # metu diena, int
        first = pd.to_datetime(date(self._year, 1, 1))
        df.loc[:, 'day_nr'] = (df['date'] - first).dt.days + 1
        df.loc[:, 'year_month'] = df['date'].dt.to_period('M').astype(str)

        # season stats
        df.loc[:, 'season_distance'] = df['distance'][::-1].cumsum()
        df.loc[:, 'season_seconds'] = df['seconds'][::-1].cumsum()
        df.loc[:, 'season_ascent'] = df['ascent'][::-1].cumsum()
        df.loc[:, 'season_per_day'] = df['season_distance'] / df['day_nr']
        df.loc[:, 'season_speed'] = self._speed(df['season_distance'], df['season_seconds'])

        # calculate goal progress
        year_len = 366 if calendar.isleap(self._year) else 365
        per_day = self._goal / year_len

        df.loc[:, 'goal_day'] = df['day_nr'] * per_day
        df.loc[:, 'goal_percent'] = (df['season_distance'] * 100) / df['goal_day']
        df.loc[:, 'goal_delta'] = df['season_distance'] - df['goal_day']

        return df.to_dict(orient='records')
