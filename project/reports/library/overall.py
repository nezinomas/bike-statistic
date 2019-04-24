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
        self.__create_years_list()
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

    def __create_pivot_table(self):
        self.__pivotTable = pd.pivot_table(
            self.__df,
            index=['bike__short_name', 'bike__date'],
            columns=['date'],
            values=['distance'],
            fill_value=0,
            aggfunc=[np.sum],
        ).sort_values('bike__date')

    def __create_years_list(self):
        self.__years = [x[-1] for x in list(self.__pivotTable.columns.values)]

    def __calc_statistic(self):
        self.__bikes = [x[0] for x in list(self.__pivotTable.index)]

        for key, bike in enumerate(self.__bikes):
            q = (
                self.__pivotTable.query("bike__short_name==['{}']".format(bike))
                .values.tolist()[0]
            )
            self.__distances.append([float(x) for x in q])
