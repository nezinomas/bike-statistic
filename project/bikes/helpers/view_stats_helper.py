import datetime

import numpy as np
import pandas as pd

from django.db.models import Sum
from django_pandas.io import read_frame

from ..models import Component
from ...reports.models import Data


class Filter(object):
    def __init__(self, bike_slug, component_filter):
        qs = self.__create_qs(bike_slug)
        self.__df = self.__create_df(qs)
        self.__components = self.__create_component_list(component_filter)

    def __create_qs(self, bike_slug):
        return Data.objects.filter(bike__slug=bike_slug).values('date', 'distance')

    def __create_df(self, qs):
        df = read_frame(qs)
        df['date'] = pd.to_datetime(df['date'])
        return df

    def __create_component_list(self, component_filter):
        if component_filter == 'all':
            r = Component.objects.prefetch_related('components').all()
        else:
            r = Component.objects.prefetch_related('components').filter(pk=component_filter)

        return r

    def total_distance(self, start_date=None, end_date=None):
        if start_date:
            df = self.__df[(self.__df['date'] > start_date) &
                           (self.__df['date'] <= end_date)]
        else:
            df = self.__df

        return df['distance'].sum()


    def component_stats_object(self):
        components_ = []
        for component in self.__components:
            km = []
            item = {}
            item['pk'] = component.pk
            item['name'] = component.name

            tmp = []
            for t_ in component.components.all():
                if not t_.end_date:
                    t_.end_date = datetime.date.today()

                k = self.total_distance(t_.start_date, t_.end_date)
                km.append(float(k))
                tmp.append(
                    {
                        'start_date': t_.start_date,
                        'end_date': t_.end_date,
                        'brand': t_.brand,
                        'price': t_.price,
                        'km': k,
                        'pk': t_.pk,
                    }
                )

            item['components'] = tmp

            stats = []
            stats.append({'label': 'avg', 'value': np.average(km) if km else 0})
            stats.append({'label': 'median', 'value': np.median(km) if km else 0})
            item['stats'] = stats

            components_.append(item)

        return {'components': components_, 'total': self.total_distance()}
