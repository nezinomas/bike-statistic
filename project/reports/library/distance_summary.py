import itertools as it
import operator

import polars as pl


class DistanceSummary():
    def __init__(self, years, bikes, data):
        self._bikes = bikes
        self._df = self._build_df(years, bikes, data)

    @property
    def table(self) -> list[dict]:
        arr =  self._df.to_dicts()
        return [
            {'year': title} | {x['bike']: x['distance'] for x in group}
            for title, group in it.groupby(arr, key=operator.itemgetter("year"))
        ]

    @property
    def total_column(self):
        df = self._df
        df = (
            df
            .groupby('year')
            .agg(pl.col('distance').sum()))
        df = df.rename({'distance': 'total'})
        return df.to_dicts()

    @property
    def total_row(self):
        df = (
            self._df
            .groupby('bike')
            .agg(pl.col('distance').sum()))
        return {x['bike']: x['distance'] for x in df.to_dicts()}

    @property
    def chart_data(self):
        return [{'name': x, 'data': self._filter_distances(x)} for x in self._bikes]

    def _filter_distances(self, bike_name):
        return (
            self._df
            .select(pl.col('distance').filter(pl.col('bike') == bike_name))
            .to_series()
            .to_list())

    def _build_df(self, years, bikes, data: list[dict]) -> pl.DataFrame:
        # product years x bikes and make [{'year': year, 'bike': bike_name}]
        arr = [{'year': r[0], 'bike': r[1]} for r in it.product(years, bikes)]
        # data frame from arr
        df1 = pl.DataFrame(arr)
        df1 = df1.with_columns([pl.col('year').cast(pl.Int32)])
        # data frame from data
        df2 = pl.DataFrame(list(data))
        df2 = (
            df2
            .with_columns([
                pl.col('date').dt.year().alias('year')
            ])
        )
        df2 = df2.drop('date')
        #
        _, df = pl.align_frames(df1, df2, on=["year", "bike"])
        return df.fill_null(0)
