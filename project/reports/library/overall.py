import pandas as pd
import numpy as np

from django_pandas.io import read_frame

from . import chart


class Overall:
    def __init__(self, model):
        qs = self.__create_query(model)
        df = self.__create_dataframe(qs)
        self.pivotTable = self.__create_pivot_table(df)

    def __create_query(self, model):
        return model.objects.values('date', 'distance', 'time', 'bike__date', 'bike__short_name')

    def __create_dataframe(self, qs):
        df = read_frame(qs)
        df['date'] = pd.to_datetime(df['date']).dt.year
        return df

    def __create_pivot_table(self, df):
        return pd.pivot_table(
            df,
            index=['bike__short_name', 'bike__date'],
            columns=['date'],
            values=['distance'],
            fill_value=0,
            aggfunc=[np.sum],
        ).sort_values('bike__date')

    def create_categories(self):
        return [x[-1] for x in list(self.pivotTable.columns.values)]

    def create_series(self):
        series = []
        bikes = [x[0] for x in list(self.pivotTable.index)]

        for key, bike in enumerate(bikes):
            item = {}
            q = self.pivotTable.query(
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
