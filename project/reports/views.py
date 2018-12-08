from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from . import forms, models


def test(request):
    return render(
        request,
        'reports/test.html',
        context={'var': 'kintamasis is view', 'var1': '? ar tikrai?'}
    )

@login_required(login_url='/admin/')
def data_table(request, start_date, end_date):
    # submit paspaustas pagrindinėje formoje
    if 'submit' in request.POST:
        formset = forms.DataFormset(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect(reverse_lazy('reports:data_table', kwargs={'start_date': start_date , 'end_date': end_date}))
    else:
        queryset = models.Data.objects.filter(date__range=(start_date, end_date))
        formset = forms.DataFormset(queryset=queryset)

    helper = forms.DataFormSetHelper()

    return render(
        request,
        "reports/data_form.html",
        {"formset": formset, 'helper': helper },
    )
