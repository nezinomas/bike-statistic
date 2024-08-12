import itertools as it

import polars as pl


class DistanceSummary:
    def __init__(self, years, bikes, data):
        self._bikes = bikes
        self._df = self._build_df(years, bikes, data)

    @property
    def table(self) -> list[dict]:
        """
        Returns a list of dictionaries representing the distance summary data grouped by year and bike.

        Returns:
            list[dict]: List of dictionaries with 'year' as a key and bike-distance mappings.

            e.g. [{'year': 2020, 'bike1': 100, 'bike2': 200}, ...]
        """

        if self._df.is_empty():
            return []

        return [
            {
                "year": year[0],
                **{x["bike"]: x["distance"] for x in data.drop("year").to_dicts()},
            }
            for year, data in self._df.group_by("year")
        ]

    @property
    def total_column(self):
        if self._df.is_empty():
            return []

        df = self._df.group_by("year").agg(pl.col("distance").sum()).sort("year")
        df = df.rename({"distance": "total"})
        return df.to_dicts()

    @property
    def total_row(self):
        if self._df.is_empty():
            return {}
        df = self._df.group_by("bike").agg(pl.col("distance").sum()).sort("bike")
        return {x["bike"]: x["distance"] for x in df.to_dicts()}

    @property
    def chart_data(self):
        return [{"name": x, "data": self._filter_distances(x)} for x in self._bikes]

    def _filter_distances(self, bike_name):
        return (
            self._df.select(pl.col("distance").filter(pl.col("bike") == bike_name))
            .to_series()
            .to_list()
        )

    def _build_years_and_bikes_df(self, years: list, bikes: list) -> pl.DataFrame:
        # product years x bikes and make [{'year': year, 'bike': bike_name}]
        arr = [
            {"year": r[0], "bike": r[1], "grp": bikes.index(r[1])}
            for r in it.product(years, bikes)
        ]
        if not arr:
            return pl.DataFrame()

        df = pl.DataFrame(arr)
        df = df.with_columns([pl.col("year").cast(pl.Int32)])

        return df

    def _build_data_df(self, data: list[dict]) -> pl.DataFrame:
        df = pl.DataFrame(list(data))
        df = df.with_columns([pl.col("date").dt.year().alias("year")])
        df = df.drop("date")
        return df

    def _build_df(self, years, bikes, data: list[dict]) -> pl.DataFrame:
        df = self._build_years_and_bikes_df(years, bikes)
        if df.is_empty():
            return df

        if not data:
            df = df.with_columns(pl.lit(0).alias("distance"))
        else:
            df_data = self._build_data_df(data)

            df = df.join(df_data, on=["year", "bike"], how="left")

        df = df.fill_null(0).sort(["year", "grp"]).drop("grp")

        return df
