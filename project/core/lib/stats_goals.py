import calendar
import datetime

import pandas as pd
from django.http import Http404
from django_pandas.io import read_frame

from ...reports.models import Data
from ...goals.models import Goal


class StatsGoals(object):
    def __init__(self, year=1970):
        self.__year = year
        self.__df = self.__create_df()
        self.__goals = self.__get_goals()

    def __create_df(self):
        qs = (
            Data.objects.
            prefetch_related('bike').
            values('id', 'date', 'bike', 'distance', 'temperature', 'time', 'ascent').
            order_by('-date').
            filter(date__year__gte=1970)
        )
        if self.__year != 1970:
            qs = qs.filter(date__year=self.__year)

        df = read_frame(qs)

        df['date'] = pd.to_datetime(df['date'])
        df['distance'] = df['distance'].astype(float)
        df['ascent'] = df['ascent'].astype(int)
        df['time'] = pd.to_timedelta(df['time'], unit='s')
        df['sec_workout'] = df['time'].dt.total_seconds()

        return df

    def __get_goals(self):
        obj = Goal.objects.filter(year__gte=1970)
        if self.__year != 1970:
            obj = obj.filter(year=self.__year)

        if not obj:
            raise Http404

        return list(obj)

    def __filter_dataframe(self, year=None):
        if year:
            start = pd.to_datetime(datetime.date(year, 1, 1))
            end = pd.to_datetime(datetime.date(year, 12, 31))
            df = self.__df[
                (self.__df['date'] >= start) & (self.__df['date'] <= end)
            ].copy()
        else:
            df = self.__df

        return df

    def __marginal_values(self, df, column, function):
        """
        df - pandas dataframe
        column - pandas dataframe column label
        function - max or min
        """

        item = {}
        try:
            choices = {
                'max': df.loc[df[column].idxmax()],
                'min': df.loc[df[column].idxmin()]
            }
            row = choices.get(function, None)
        except:
            return item

        if row is not None:
            date_column = '{}_{}_date'.format(function, column)
            value_column = '{}_{}_value'.format(function, column)

            item[date_column] = row.date
            item[value_column] = row[column]

        return item

    def __calc_speed(self, df):
        df.loc[:, 'speed'] = (
            df['distance'] /
            (df['sec_workout'] / 3600)
        )

    def stats(self, year=None):
        df = self.__filter_dataframe(year)

        if df.empty:
            return None

        self.__calc_speed(df)

        max_temp = self.__marginal_values(df, 'temperature', 'max')
        min_temp = self.__marginal_values(df, 'temperature', 'min')
        max_ascent = self.__marginal_values(df, 'ascent', 'max')
        max_dist = self.__marginal_values(df, 'distance', 'max')
        speed = self.__marginal_values(df, 'speed', 'max')

        return dict(**max_temp, **min_temp, **max_ascent, **speed, **max_dist)

    def total_distance(self, year=None):
        df = self.__filter_dataframe(year)
        return df['distance'].sum()

    def objects(self):
        retVal = []
        for goal in self.__goals:
            item = {}
            item['id'] = goal.id
            item['year'] = goal.year
            item['goal'] = goal.goal
            item['distance'] = self.total_distance(goal.year)
            item['stats'] = self.stats(goal.year)

            retVal.append(item)

        return retVal

    def table(self):
        df = self.__filter_dataframe(self.__year)

        if df.empty:
            return None

        # metu diena, int
        first = pd.to_datetime(datetime.date(self.__year, 1, 1))
        days = 366 if calendar.isleap(self.__year) else 365
        per_day = self.__goals[0].goal / days

        df.loc[:, 'day_num'] = (df['date'] - first).dt.days + 1
        df.loc[:, 'year_month'] = df['date'].dt.to_period('M').astype(str)

        df.loc[:, 'speed_workout'] = df['distance'] / (df['sec_workout'] / 3600)

        df.loc[:, 'distance_season'] = df['distance'][::-1].cumsum()
        df.loc[:, 'sec_season'] = df['sec_workout'][::-1].cumsum()
        df.loc[:, 'ascent_season'] = df['ascent'][::-1].cumsum()
        df.loc[:, 'speed_season'] = df['distance_season'] / (df['sec_season'] / 3600)
        df.loc[:, 'per_day_season'] = df['distance_season'] / df['day_num']

        df.loc[:, 'day_goal'] = df['day_num'] * per_day
        df.loc[:, 'percent'] = (df['distance_season'] * 100) / df['day_goal']
        df.loc[:, 'km_delta'] = df['distance_season'] - df['day_goal']

        return df.to_dict(orient='records')

    def month_table(self):
        s_date = datetime.date(self.__year, 1, 1)
        e_date = datetime.date(self.__year, 12, 31)
        df = self.__filter_dataframe(s_date, e_date)

        df.index = df['date']
        df = df.resample('M').sum()

        df.loc[:, 'speed_month'] = df['distance'] / (df['sec_workout'] / 3600)
        df.loc[:, 'year_month'] = pd.to_datetime(df.index.values).to_period('M')
        df.loc[:, 'days_in_month'] = pd.to_datetime(df.index.values).day
        df.loc[:, 'per_day_month'] = df['distance'] / df['days_in_month']
        df.loc[:, 'speed_month'] = df['distance'] / (df['sec_workout'] / 3600)

        df.reset_index()
        df.index = df['year_month']
        df.index = df.index.astype(str)

        return df.to_dict('index')
