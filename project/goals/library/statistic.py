import datetime
import calendar
import numpy as np
import pandas as pd

from django_pandas.io import read_frame
from django.shortcuts import get_object_or_404

from ..models import Goal
from ...reports.models import Data

class Statistic(object):
    def __init__(self, year='all'):
        qs = self.__create_qs()
        self.__year = year
        self.__df = self.__create_df(qs)
        self.__goals = self.__create_objects(year)

    def __create_qs(self):
        return Data.objects.\
            prefetch_related('bike').\
            values('id', 'date', 'bike', 'distance', 'temperature', 'time').\
            order_by('date')

    def __create_df(self, qs):
        df = read_frame(qs)

        df['date'] = pd.to_datetime(df['date'])
        df['distance'] = df['distance'].astype(float)
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
                (self.__df['date'] >= start_date)
                & (self.__df['date'] <= end_date)
            ].copy()
        else:
            df = self.__df

        return df

    def stats(self, start_date=None, end_date=None):
        item = {}
        df = self.__filter_dataframe(start_date, end_date)

        try:
            row = df.loc[df['temperature'].idxmax()]
            item['max_temp_date'] = row.date
            item['max_temp_value'] = row.temperature
        except:
            pass

        try:
            row = df.loc[df['temperature'].idxmin()]
            item['min_temp_date'] = row.date
            item['min_temp_value'] = row.temperature
        except:
            pass

        return item

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
        s_date = pd.to_datetime(datetime.date(self.__year, 1, 1))
        e_date = pd.to_datetime(datetime.date(self.__year, 12, 31))
        df = self.__filter_dataframe(s_date, e_date)

        # metu diena, int
        first = pd.to_datetime(datetime.date(self.__year, 1, 1))
        days = 366 if calendar.isleap(self.__year) else 365
        per_day = self.__goals.goal/days

        df.loc[:, 'day_num'] = (df['date'] - first).dt.days + 1
        df.loc[:, 'year_month'] = df['date'].dt.to_period('M').astype(str)
        df.loc[:, 'temperature'] = df['temperature'].replace({pd.np.nan: None})

        df.loc[:, 'speed_workout'] = df['distance']/(df['sec_workout']/3600)

        df.loc[:, 'distance_season'] = df['distance'].cumsum()
        df.loc[:, 'sec_season'] = df['sec_workout'].cumsum()
        df.loc[:, 'speed_season'] = df['distance_season']/(df['sec_season']/3600)
        df.loc[:, 'per_day_season'] = df['distance_season']/df['day_num']

        df.loc[:, 'day_goal'] = df['day_num']*per_day
        df.loc[:, 'percent'] = (df['distance_season']*100)/df['day_goal']
        df.loc[:, 'km_delta'] = df['distance_season']-df['day_goal']

        # False kada keičiasi mėnuo
        df.loc[:, 'match'] = df.year_month.eq(df.year_month.shift())
        df.loc[df.index[0], 'match'] = True # pirma eilute visada yra False; pakeiciu

        return df.to_dict(orient='records')

    def month_table(self):
        s_date = pd.to_datetime(datetime.date(self.__year, 1, 1))
        e_date = pd.to_datetime(datetime.date(self.__year, 12, 31))
        df = self.__filter_dataframe(s_date, e_date)

        df.index = df['date']
        df = df.resample('M').sum()

        df.loc[:, 'speed_month'] = df['distance'] / (df['sec_workout']/3600)
        df.loc[:, 'year_month'] = pd.to_datetime(df.index.values).to_period('M')
        df.loc[:, 'days_in_month'] = pd.to_datetime(df.index.values).day
        df.loc[:, 'per_day_month'] = df['distance']/df['days_in_month']
        df.loc[:, 'speed_month'] = df['distance']/(df['sec_workout']/3600)

        df.reset_index()
        df.index = df['year_month']
        df.index = df.index.astype(str)

        return df.to_dict('index')
