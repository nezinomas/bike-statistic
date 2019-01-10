from django.shortcuts import reverse, render, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse

from .models import Bike, Component, ComponentStatistic
from .forms import ComponentForm

from ..reports.models import Data


def index(request):
    return render(
        request,
        'bikes/index.html',
        context={'var': 'kintamasis is view', 'var1': '? ar tikrai?'}
    )


def save_component(request, context, form, template_name):
    data = {}

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            components = Component.objects.all()
            data['html_list'] = render_to_string(
                'bikes/includes/partial_component_list.html', {'components': components})
        else:
            data['form_is_valid'] = False

    context['form'] = form
    data['html_form'] = render_to_string(
        template_name=template_name,
        context=context,
        request=request
    )

    return JsonResponse(data)


def component_list(request):
    components = Component.objects.all()
    return render(request, 'bikes/component_list.html', {'components': components})


def component_create(request):
    form = ComponentForm(request.POST or None)
    context = {'url': reverse('bikes:component_create')}
    return save_component(request, context, form, 'bikes/includes/partial_component_update.html')


def component_update(request, pk):
    component = get_object_or_404(Component, pk=pk)
    form = ComponentForm(request.POST or None, instance=component)
    context = {'url': reverse('bikes:component_update', kwargs={'pk': pk})}
    return save_component(request, context, form, 'bikes/includes/partial_component_update.html')


def component_delete(request, pk):
    component = get_object_or_404(Component, pk=pk)
    data = {}

    if request.method == 'POST':
        component.delete()
        data['form_is_valid'] = True
        components = Component.objects.all()
        data['html_list'] = render_to_string('bikes/includes/partial_component_list.html', {'components': components})
    else:
        context = {'component':component}
        data['html_form'] = render_to_string('bikes/includes/partial_component_delete.html', context=context, request=request)

    return JsonResponse(data)


import pandas as pd
import numpy as np

from django_pandas.io import read_frame
from django.db.models import Sum
import datetime


class Filter(object):
    def __init__(self, qs):
        self.__df = self.__create_df(qs)

    def __create_df(self, qs):
        df = read_frame(qs)
        df['date'] = pd.to_datetime(df['date'])
        return df

    def total_distance(self, start_date = None, end_date = None):
        if start_date:
            df = self.__df[(self.__df['date'] > start_date) & (self.__df['date'] <= end_date)]
        else:
            df = self.__df

        return df['distance'].sum()



def bike_component_list(request, bike):
    qs = Data.objects.filter(bike__slug=bike).values('date', 'distance')

    obj = Filter(qs)



    components = Component.objects.prefetch_related('components').all()

    components_ = []
    for component in components:
        km = []
        item = {}
        item['pk'] = component.pk
        item['name'] = component.name

        tmp = []
        for t_ in component.components.all():
            if not t_.end_date:
                t_.end_date = datetime.date.today()

            k = obj.total_distance(t_.start_date, t_.end_date)
            km.append(float(k))
            tmp.append(
                {
                    'start_date': t_.start_date,
                    'end_date': t_.end_date,
                    'brand': t_.brand,
                    'price': t_.price,
                    'km': k,
                }
            )

        item['components'] = tmp

        stats = []
        stats.append({'label': 'avg', 'value': np.average(km)})
        stats.append({'label': 'median', 'value': np.median(km)})
        item['stats'] = stats

        components_.append(item)

    return render(request, 'bikes/bike_component_list.html', {'components': components_, 'total': obj.total_distance()})

