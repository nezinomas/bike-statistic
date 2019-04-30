import numpy as np
import pandas as pd
from django_pandas.io import read_frame

from ..models import Data


class Overall(object):
    def __init__(self):
        self.__years = []
        self.__distances = []
        self.__bikes = []

        self.__create_dataframe()
        self.__create_pivot_table()
        self.__calc_statistic()

    @property
    def df(self):
        return self.__df

    @property
    def years(self):
        return self.__years

    @property
    def distances(self):
        return self.__distances

    @property
    def bikes(self):
        return self.__bikes

    def __create_query(self):
        return Data.objects.values(
            'date',
            'distance',
            'time',
            'bike__date',
            'bike__short_name'
        )

    def __create_dataframe(self):
        qs = self.__create_query()

        if not qs:
            raise Exception('No data in db.')

        self.__df = read_frame(qs)
        self.__df['date'] = pd.to_datetime(self.__df['date']).dt.year
        self.__df['distance'] = self.__df['distance'].astype(float)

    def __create_pivot_table(self):
        self.__pivotTable = pd.pivot_table(
            self.__df,
            index=['bike__short_name', 'bike__date'],
            columns=['date'],
            values=['distance'],
            fill_value=0,
            aggfunc=[np.sum],
        ).sort_values('bike__date').reset_index().set_index('bike__short_name')

        self.__pivotTable.drop(columns=['bike__date'], inplace=True)

    def __calc_statistic(self):
        data = self.__pivotTable.to_dict('split')

        self.__bikes = data['index']
        self.__distances = data['data']
        self.__years = list(self.__pivotTable.columns.levels[2])[:-1]
