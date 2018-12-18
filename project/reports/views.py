import json
from calendar import monthrange
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy

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

    # backgroundColor: [
    #     'rgba(255, 99, 132, 0.2)',
    #     'rgba(54, 162, 235, 0.2)',
    #     'rgba(255, 206, 86, 0.2)',
    #     'rgba(75, 192, 192, 0.2)',
    #     'rgba(153, 102, 255, 0.2)',
    #     'rgba(255, 159, 64, 0.2)'
    # ],
    # borderColor: [
    #     'rgba(255,99,132,1)',
    #     'rgba(54, 162, 235, 1)',
    #     'rgba(255, 206, 86, 1)',
    #     'rgba(75, 192, 192, 1)',
    #     'rgba(153, 102, 255, 1)',
    #     'rgba(255, 159, 64, 1)'
    # ],
    chart = {'first': {
        'xAxis': {'categories': ['Africa', 'America', 'Asia', 'Europe', 'Oceania']},
        'series': [
            {
            'name': 'Year 1800',
            'data': [107, 31, 635, 203, 2],
            'color': 'rgba(255, 99, 132, 0.5)',
            'borderColor': 'rgba(255,99,132,0.5)',
            'borderWidth:': '0.25',

            },
            {
            'name': 'Year 1900',
            'data': [133, 156, 947, 408, 6],
            'color': 'rgba(54, 162, 235, 0.5)',
            'borderColor': 'rgba(54, 162, 235, 0.5)',
            'borderWidth:': '0.25',
            },
            {
            'name': 'Year 2012',
            'data': [1052, 954, 4250, 740, 38],
            'color': 'rgba(255, 206, 86, 0.5)',
            'borderColor': 'rgba(255, 206, 86, 0.5)',
            'borderWidth:': '0.25',
            },
        ]
    }}

    return JsonResponse(chart)


def charts(request):
    return render(request, template_name='reports/charts.html', context={'customers': 15})
