import datetime

import numpy as np
import pandas as pd

from django.db.models import Prefetch
from django_pandas.io import read_frame

from ..models import Component, ComponentStatistic
from ...reports.models import Data


class Filter(object):
    def __init__(self, bike_slug, component_filter):
        qs = self.__create_qs(bike_slug)
        self.__df = self.__create_df(qs)
        self.__components = self.__get_objects(bike_slug, component_filter)

    def __create_qs(self, bike_slug):
        return Data.objects.\
            filter(bike__slug=bike_slug).\
            values('date', 'distance')

    def __create_df(self, qs):
        df = read_frame(qs)
        df['date'] = pd.to_datetime(df['date'])
        return df

    def __get_objects(self, bike_slug, component_filter):
        filter_bike = ComponentStatistic.objects.filter(bike__slug=bike_slug)
        prefetch = Prefetch('components', queryset=filter_bike)

        if component_filter == 'all':
            r = Component.objects.\
                prefetch_related(prefetch).\
                all()
        else:
            r = Component.objects.\
                prefetch_related(prefetch).\
                filter(pk=component_filter)

        return r

    def __totals(self):
        retVal = []
        retVal.append({'label': 'avg', 'value': np.average(self.__km) if self.__km else 0})
        retVal.append({'label': 'median', 'value': np.median(self.__km) if self.__km else 0})
        return retVal

    def __format_dictionary(self, items):
        retVal = []

        for item in items:
            if not item.end_date:
                item.end_date = datetime.date.today()

            km = self.total_distance(item.start_date, item.end_date)
            retVal.append(
                {
                    'start_date': item.start_date,
                    'end_date': item.end_date,
                    'brand': item.brand,
                    'price': item.price,
                    'km': km,
                    'pk': item.pk,
                }
            )
            self.__km.append(float(km))

        return retVal

    def total_distance(self, start_date=None, end_date=None):
        if start_date:
            df = self.__df[
                (self.__df['date'] > pd.to_datetime(start_date))
                & (self.__df['date'] <= pd.to_datetime(end_date))
            ]
        else:
            df = self.__df

        return df['distance'].sum()

    def components(self):
        retVal = []
        for component in self.__components:
            self.__km = []
            item = {}
            item['pk'] = component.pk
            item['name'] = component.name
            item['components'] = self.__format_dictionary(component.components.all())
            item['stats'] = self.__totals()

            retVal.append(item)

        return retVal