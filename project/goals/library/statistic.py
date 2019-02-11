import calendar
import datetime
import pandas as pd

from django.shortcuts import get_object_or_404
from django_pandas.io import read_frame

from ...reports.models import Data
from ..models import Goal


class Statistic(object):
    def __init__(self, year='all'):
        qs = self.__create_qs()
        self.__year = year
        self.__df = self.__create_df(qs)
        self.__goals = self.__create_objects(year)

    def __create_qs(self):
        return Data.objects.\
            prefetch_related('bike').\
            values('id', 'date', 'bike', 'distance', 'temperature', 'time', 'ascent').\
            order_by('date')

    def __create_df(self, qs):
        df = read_frame(qs)

        df['date'] = pd.to_datetime(df['date'])
        df['distance'] = df['distance'].astype(float)
        df['ascent'] = df['ascent'].astype(int)
        df['time'] = pd.to_timedelta(df['time'], unit='s')
        df['sec_workout'] = df['time'].dt.total_seconds()

        return df

    def __create_objects(self, year='all'):
        if year == 'all':
            obj = Goal.objects.all()
        else:
            obj = get_object_or_404(Goal, year=year)

        return obj

    def __filter_dataframe(self, start_date, end_date):
        if start_date:
            df = self.__df[
                (self.__df['date'] >= pd.to_datetime(start_date))
                & (self.__df['date'] <= pd.to_datetime(end_date))
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

    def __average_speed(self, df):
        d = df.copy()
        d.loc[:, 'speed'] = d['distance'] / \
            (d['sec_workout'] / 3600)

        row = d.loc[d['speed'].idxmax()]

        return {
            'max_speed_date': row.date,
            'max_speed_value': row.speed
        }

    def stats(self, start_date=None, end_date=None):
        df = self.__filter_dataframe(start_date, end_date)

        max_temp = self.__marginal_values(df, 'temperature', 'max')
        min_temp = self.__marginal_values(df, 'temperature', 'min')
        max_ascent = self.__marginal_values(df, 'ascent', 'max')
        max_dist = self.__marginal_values(df, 'distance', 'max')
        speed = self.__average_speed(df)

        return dict(**max_temp, **min_temp, **max_ascent, **speed, **max_dist)

    def total_distance(self, start_date=None, end_date=None):
        df = self.__filter_dataframe(start_date, end_date)
        return df['distance'].sum()

    def objects(self):
        retVal = []
        for year in self.__goals:
            item = {}
            item['id'] = year.id
            item['pk'] = year.pk
            item['year'] = year.year
            item['goal'] = year.goal
            item['distance'] = self.total_distance(
                datetime.date(year.year, 1, 1),
                datetime.date(year.year, 12, 31)
            )
            item['stats'] = self.stats(
                datetime.date(year.year, 1, 1),
                datetime.date(year.year, 12, 31)
            )
            retVal.append(item)

        return retVal

    def table(self):
        s_date = datetime.date(self.__year, 1, 1)
        e_date = datetime.date(self.__year, 12, 31)
        df = self.__filter_dataframe(s_date, e_date)

        # metu diena, int
        first = pd.to_datetime(datetime.date(self.__year, 1, 1))
        days = 366 if calendar.isleap(self.__year) else 365
        per_day = self.__goals.goal / days

        df.loc[:, 'day_num'] = (df['date'] - first).dt.days + 1
        df.loc[:, 'year_month'] = df['date'].dt.to_period('M').astype(str)
        # df.loc[:, 'temperature'] = df['temperature'].replace({pd.np.nan: None})

        df.loc[:, 'speed_workout'] = df['distance'] / (df['sec_workout'] / 3600)

        df.loc[:, 'distance_season'] = df['distance'].cumsum()
        df.loc[:, 'sec_season'] = df['sec_workout'].cumsum()
        df.loc[:, 'ascent_season'] = df['ascent'].cumsum()
        df.loc[:, 'speed_season'] = df['distance_season'] / (df['sec_season'] / 3600)
        df.loc[:, 'per_day_season'] = df['distance_season'] / df['day_num']

        df.loc[:, 'day_goal'] = df['day_num'] * per_day
        df.loc[:, 'percent'] = (df['distance_season'] * 100) / df['day_goal']
        df.loc[:, 'km_delta'] = df['distance_season'] - df['day_goal']

        # False kada keičiasi mėnuo
        df.loc[:, 'match'] = df.year_month.eq(df.year_month.shift())
        df.loc[df.index[0], 'match'] = True  # pirma eilute visada yra False; pakeiciu

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
