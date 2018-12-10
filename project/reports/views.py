from datetime import datetime, timedelta
from calendar import monthrange

from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required

from .endomondo.endomondo import MobileApi

from . import forms, models
from ..bikes import models as bike_models

from ..config.secrets import get_secret


def test(request):

    endomondo = MobileApi(email=get_secret("ENDOMONDO_USER"), password=get_secret("ENDOMONDO_PASS"))
    auth_token = endomondo.get_auth_token()    

    workouts = endomondo.get_workouts(maxResults=2)

    bike = bike_models.Bike.objects.get(pk=1)
    
    # for w in workouts:
    #     if w.sport == 2:

    #         models.Data.objects.create(
    #             bike=bike,
    #             date=w.start_time,
    #             distance=w.distance,
    #             time=timedelta(seconds=w.duration),
    #             ascent=w.ascent,
    #             descent=w.descent,
    #         )

    return render(
        request,
        'reports/test.html',
        context={'var': 'kintamasis is view', 'var1': '? ar tikrai?'}
    )


# @login_required(login_url='/admin/')
def data_table(request, start_date, end_date):
    # paspaustas filter mygtukas
    if 'date_filter' in request.POST:
        filter_form = forms.DateFilterForm(request.POST)
        if filter_form.is_valid():
            data = filter_form.cleaned_data
            url = reverse_lazy('reports:data_table', kwargs={'start_date': data['start_date'] , 'end_date': data['end_date']})
            return redirect(url)

    # submit paspaustas pagrindinėje formoje
    if 'submit' in request.POST:
        formset = forms.DataFormset(request.POST)
        if formset.is_valid():
            formset.save()
            url = reverse_lazy('reports:data_table', kwargs={'start_date': start_date , 'end_date': end_date})
            return redirect(url)
    else:
        queryset = models.Data.objects.filter(date__range=(start_date, end_date))
        formset = forms.DataFormset(queryset=queryset)

    helper = forms.DataFormSetHelper()

    filter_form = forms.DateFilterForm(initial={'start_date': start_date, 'end_date': end_date})

    return render(
        request,
        "reports/data_form.html",
        {"formset": formset, 'helper': helper, 'filter_form': filter_form },
    )


# @login_required(login_url='/admin/')
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


# @login_required(login_url='/admin/')
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
