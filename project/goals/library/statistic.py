import datetime
import numpy as np
import pandas as pd

from django_pandas.io import read_frame

from ..models import Goal
from ...reports.models import Data

class Statistic(object):
    def __init__(self, year='all'):
        qs = self.__create_qs()
        self.__df = self.__create_df(qs)
        self.__years = self.__create_objects(year)

    def __create_qs(self):
        return Data.objects.prefetch_related('bike_set').all().order_by('date')

    def __create_df(self, qs):
        df = read_frame(qs)
        df['date'] = pd.to_datetime(df['date'])

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
            ]
        else:
            df = self.__df

        return df

    def stats(self, start_date=None, end_date=None):
        item = {}
        df = self.__filter_dataframe(start_date, end_date)

        row = df.loc[df['temperature'].idxmax()]
        item['max_temp_date'] = row.date
        item['max_temp_value'] = row.temperature

        row = df.loc[df['temperature'].idxmin()]
        item['min_temp_date'] = row.date
        item['min_temp_value'] = row.temperature

        return item

    def total_distance(self, start_date=None, end_date=None):
        df = self.__filter_dataframe(start_date, end_date)
        return df['distance'].sum()

    def objects(self):
        retVal = []
        for year in self.__years:
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

