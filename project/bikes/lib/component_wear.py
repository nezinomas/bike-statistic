from datetime import datetime

import numpy as np
import polars as pl


class ComponentWear:
    def __init__(self, stats, data):
        self._stats = pl.DataFrame(stats)
        self._data = pl.DataFrame(data)
        self._df = self._make_df()

    @property
    def component_km(self):
        dicts = self._df.to_dicts()
        return dicts[0] if dicts else []

    def _make_df(self):
        if self._stats.is_empty():
            return pl.DataFrame()

        # fill empty end_date and convert back to list[dict]
        stats = (
            self._stats
            .with_column(
                pl.col('end_date').fill_null(datetime.now().date())
            ).to_dicts())

        if self._data.is_empty():
            return pl.DataFrame({str(x['pk']): 0 for x in stats})

        filter_and_sum = [self._sum_distances(
            x['start_date'], x['end_date'], x['pk']) for x in stats]

        return self._data.select(filter_and_sum)

    def _sum_distances(self, start, end, name):
        return (
            pl.col('distance')
            .filter(pl.col('date').is_between(start, end, closed='both'))
            .sum()
            .alias(f'{name}'))

    @property
    def bike_km(self):
        try:
            km = self._data.select(pl.col('distance').sum()).to_numpy()[0,0]
        except (AttributeError, pl.exceptions.NotFoundError):
            km = 0
        return km

    @property
    def component_stats(self):
        dicts = {'avg': 0, 'median': 0,}
        if not self._df.is_empty():
            col = self._df.transpose()
            dicts['avg'] = np.average(col)
            dicts['median'] = np.median(col)

        return dicts
