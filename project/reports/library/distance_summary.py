import pandas as pd


class DistanceSummary():
    def __init__(self, years, bikes, data):
        self._bikes = bikes
        self._df = self._build_df(years, data)

    @property
    def table(self):
        df = self._df.copy()
        df.reset_index(inplace=True)

        return df.to_dict('records')

    @property
    def total_column(self):
        df = self._df.copy()

        # calculate total value for every row
        df.loc[:, 'total'] = df.sum(axis=1)

        df.reset_index(inplace=True)

        return df[['year', 'total']].to_dict('records')

    @property
    def total_row(self):
        df = self._df.copy()

        # calculate total values for all columns
        df.loc['total', :] = df.sum(axis=0)

        # select total row
        df = df.loc['total':]

        return df.to_dict('records')[0]

    @property
    def chart_data(self):
        df = self._df.copy()

        r = []
        for bike in self._bikes:
            r.append({
                'name': bike,
                'data': df[bike].values.tolist()
            })

        return r

    def _build_df(self, years, data):
        # create rows from years
        df = pd.DataFrame({'year': pd.Series(years)})

        # create columns from bikes
        for bike in self._bikes:
            df[bike] = 0.0

        df.set_index('year', inplace=True)

        # copy values from data
        for row in data:
            df.at[row['date'].year, row['bike']] = row['distance']

        # sort index and replace nan->0.0
        df.sort_index(inplace=True)
        df.fillna(value=0.0, inplace=True)

        return df
