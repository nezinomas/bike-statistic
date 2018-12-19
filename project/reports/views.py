import json
import numpy as np
import pandas as pd

from calendar import monthrange
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy

from django_pandas.io import read_frame

from . import forms, models

from .library.insert_data import insert_data as inserter


def test(request):

    return render(
        request,
        'reports/test.html',
        context={'var': 'kintamasis is view', 'var1': '? ar tikrai?'}
    )


@login_required()
def data_table(request, start_date, end_date):
    # paspaustas filter mygtukas
    if 'date_filter' in request.POST:
        filter_form = forms.DateFilterForm(request.POST)
        if filter_form.is_valid():
            data = filter_form.cleaned_data
            url = reverse_lazy('reports:data_table', kwargs={'start_date': data['start_date'], 'end_date': data['end_date']})
            return redirect(url)

    # submit paspaustas pagrindinėje formoje
    if 'submit' in request.POST:
        formset = forms.DataFormset(request.POST)
        if formset.is_valid():
            formset.save()
            url = reverse_lazy('reports:data_table', kwargs={'start_date': start_date, 'end_date': end_date})
            return redirect(url)
    else:
        queryset = models.Data.objects.filter(date__range=(start_date, end_date))
        formset = forms.DataFormset(queryset=queryset)

    helper = forms.DataFormSetHelper()

    filter_form = forms.DateFilterForm(initial={'start_date': start_date, 'end_date': end_date})

    return render(
        request,
        "reports/data_form.html",
        {"formset": formset, 'helper': helper, 'filter_form': filter_form},
    )


@login_required()
def data_table_empty_date(request):
    now = datetime.now()
    return redirect(
        reverse(
            'reports:data_table',
            kwargs={
                'start_date': '{y}-{m}-{d}'.format(y=now.year, m=now.month, d='01'),
                'end_date': '{y}-{m}-{d}'.format(y=now.year, m=now.month, d=monthrange(now.year, now.month)[1]),
            }
        )
    )


@login_required()
def data_table_no_end(request, start_date):
    now = datetime.now()
    return redirect(
        reverse(
            'reports:data_table',
            kwargs={
                'start_date': start_date,
                'end_date': '{y}-{m}-{d}'.format(y=now.year, m=now.month, d=monthrange(now.year, now.month)[1]),
            }
        )
    )


@login_required()
def insert_data(request):
    try:
        inserter(4)
        message = 'ok'
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)

    return render(request, template_name='reports/get_data.html', context={'message': message})


def get_data(request):

    qs = models.Data.objects.values('date', 'distance', 'time', 'bike__date', 'bike__short_name')

    df = read_frame(qs)
    df['date'] = pd.to_datetime(df['date']).dt.year

    pivotTable = pd.pivot_table(
        df,
        index=['bike__short_name', 'bike__date'],
        columns=['date'],
        values=['distance'],
        fill_value=0,
        aggfunc=[np.sum],
    ).sort_values('bike__date')

    backgroundColor = [
        'rgba(255, 99, 132, 0.35)',
        'rgba(54, 162, 235, 0.35)',
        'rgba(255, 206, 86, 0.35)',
        'rgba(75, 192, 192, 0.35)',
        'rgba(153, 102, 255, 0.35)',
        'rgba(200, 200, 200, 0.35)'
    ]
    borderColor = [
        'rgba(255,99,132, 0.85)',
        'rgba(54, 162, 235, 0.85)',
        'rgba(255, 206, 86, 0.85)',
        'rgba(75, 192, 192, 0.85)',
        'rgba(153, 102, 255, 0.85)',
        'rgba(200, 200, 200, 0.85)'
    ]


    series = []

    bikes = [x[0] for x in list(pivotTable.index)]

    for key, bike in enumerate(bikes):
        item = {}
        q = pivotTable.query("bike__short_name==['{}']".format(bike)).values.tolist()[0]

        item = {
                'name': bike,
                'data': [float(x) for x in q],
                'color': backgroundColor[key],
                'borderColor': borderColor[key],
                'borderWidth:': '0.25',
            }

        series.append(item)

    categories = [x[-1] for x in list(pivotTable.columns.values)]


    chart = {'first': {
        'xAxis': {'categories': categories},
        'series': series[::-1]
    }}

    return JsonResponse(chart)


def charts(request):
    return render(request, template_name='reports/charts.html', context={'customers': 15})
