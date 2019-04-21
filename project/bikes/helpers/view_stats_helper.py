import datetime

import numpy as np
import pandas as pd
from django.db.models import Prefetch
from django.http import Http404
from django_pandas.io import read_frame

from ...reports.models import Data
from ..models import Component, ComponentStatistic


class Filter(object):
    def __init__(self, bike_slug, component_pk):
        self.__bike_slug = bike_slug
        self.__component_pk = component_pk

        self.__df = None
        self.__component = None
        self.__components_list = []
        self.__components_stats = {}
        self.__distances = []

        self.__create_df()
        self.__get_component()
        self.__get_components_list()
        self.__calc_components_stats()

    @property
    def component(self):
        return self.__component

    @property
    def components_list(self):
        return self.__components_list

    @property
    def components_stats(self):
        return self.__components_stats

    def __create_qs(self):
        return Data.objects.\
            filter(bike__slug=self.__bike_slug).\
            values('date', 'distance')

    def __create_df(self):
        qs = self.__create_qs()

        self.__df = read_frame(qs)
        self.__df['date'] = pd.to_datetime(self.__df['date'])

    def __get_component(self):
        filter_bike = ComponentStatistic.objects.filter(bike__slug=self.__bike_slug)
        prefetch = Prefetch('components', queryset=filter_bike)

        component = (
            Component.objects.
            prefetch_related(prefetch).
            filter(pk=self.__component_pk)
        )
        if not component:
            raise Http404

        self.__component = [*component][0]

    def __get_components_list(self):
        for item in self.__component.components.all():
            if not item.end_date:
                item.end_date = datetime.date.today()

            km = self.total_distance(item.start_date, item.end_date)
            self.__components_list.append(
                {
                    'start_date': item.start_date,
                    'end_date': item.end_date,
                    'brand': item.brand,
                    'price': item.price,
                    'km': km,
                    'pk': item.pk,
                }
            )
            self.__distances.append(float(km))

    def __calc_components_stats(self):
        self.__components_stats = {
            'avg': np.average(self.__distances) if self.__distances else 0,
            'median': np.median(self.__distances) if self.__distances else 0
        }

    def total_distance(self, start_date=None, end_date=None):
        if start_date:
            df = self.__df[
                (self.__df['date'] >= pd.to_datetime(start_date)) &
                (self.__df['date'] <= pd.to_datetime(end_date))
            ]
        else:
            df = self.__df

        return df['distance'].sum()
