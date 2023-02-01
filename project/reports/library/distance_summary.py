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
        if self._df.is_empty():
            return []

        df = (
            self._df
            .groupby('year')
            .agg(pl.col('distance').sum())
            .sort('year'))
        df = df.rename({'distance': 'total'})
        return df.to_dicts()

    @property
    def total_row(self):
        if self._df.is_empty():
            return {}
        df = (
            self._df
            .groupby('bike')
            .agg(pl.col('distance').sum())
            .sort('bike'))
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

    def _build_years_and_bikes_df(self, years: list, bikes: list) -> pl.DataFrame:
        # product years x bikes and make [{'year': year, 'bike': bike_name}]
        arr = [{'year': r[0], 'bike': r[1]} for r in it.product(years, bikes)]
        if not arr:
            return pl.DataFrame()
        df = pl.DataFrame(arr)
        df = df.with_columns([pl.col('year').cast(pl.Int32)])
        return df

    def _build_data_df(self, data: list[dict]) -> pl.DataFrame:
        df = pl.DataFrame(list(data))
        df = (
            df
            .with_columns([
                pl.col('date').dt.year().alias('year')
            ])
        )
        df = df.drop('date')
        return df

    def _build_df(self, years, bikes, data: list[dict]) -> pl.DataFrame:
        df1 = self._build_years_and_bikes_df(years, bikes)
        if df1.is_empty():
            return df1
        df2 = self._build_data_df(data)
        _, df = pl.align_frames(df1, df2, on=["year", "bike"])
        return df.fill_null(0)
