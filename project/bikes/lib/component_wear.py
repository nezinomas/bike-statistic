from datetime import date

import numpy as np
import pandas as pd
from pandas import DataFrame as DF


class ComponentWear:
    def __init__(self, components, data):
        data = self._convert_to_values(data)
        components = self._convert_to_values(components)

        self._components = components

        df = self._build_df(data)
        self._component_km = self._get_component_km(df)

    @property
    def component_km(self):
        return self._component_km

    @property
    def bike_km(self):
        values = list(self._component_km.values())
        km = pd.Series(values, dtype=float)

        return np.sum(km) if not km.empty else 0

    @property
    def component_stats(self):
        values = list(self._component_km.values())
        km = pd.Series(values, dtype=float)

        return {
            'avg': np.average(km) if not km.empty else 0,
            'median': np.median(km) if not km.empty else 0,
        }

    def _build_df(self, data):
        if not data:
            return DF()

        df = DF(data)

        df['date'] = pd.to_datetime(df['date'])

        return df

    def _convert_to_values(self, query_set):
        try:
            final = query_set.values()
        except:
            final = query_set

        return final

    def _get_component_km(self, data):
        if not self._components:
            return {}

        final = {}

        df = data.copy()

        for row in self._components:
            _df = self._filter(df, row['start_date'], row['end_date'])

            km = _df['distance'].sum() if not _df.empty else 0

            final[row['id']] = km

        return final

    def _filter(self, df, start, end):
        if df.empty:
            return df

        if not end:
            end = date.today()

        qte = df['date'] >= pd.to_datetime(start)
        lte = df['date'] <= pd.to_datetime(end)

        df = df[qte & lte]  # filter df

        return df
