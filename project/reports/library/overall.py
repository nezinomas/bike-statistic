import numpy as np
import pandas as pd
from django_pandas.io import read_frame

from . import chart
from ..models import Data


class Overall(object):
    def __init__(self):
        self.__create_dataframe()
        self.__create_pivot_table()

    @property
    def df(self):
        return self.__df

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

    def create_categories(self):
        return [x[-1] for x in list(self.__pivotTable.columns.values)]

    def create_series(self):
        series = []
        bikes = [x[0] for x in list(self.__pivotTable.index)]

        for key, bike in enumerate(bikes):
            item = {}
            q = self.__pivotTable.query(
                "bike__short_name==['{}']".format(bike)).values.tolist()[0]

            item = {
                'name': bike,
                'data': [float(x) for x in q],
                'color': chart.get_color(key, 0.35),
                'borderColor': chart.get_color(key, 0.85),
                'borderWidth:': '0.25',
            }
            series.append(item)

        return series
