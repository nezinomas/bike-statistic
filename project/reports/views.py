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
def data_table(request, year, month):
    # submit paspaustas pagrindinėje formoje
    if 'submit' in request.POST:
        formset = forms.DataFormset(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect(reverse_lazy('reports:data_table', kwargs={'year': year , 'month': month}))
    else:
        queryset = models.Data.objects.filter(date__year=year).filter(date__month=month)
        formset = forms.DataFormset(queryset=queryset)

    helper = forms.DataFormSetHelper()

    return render(
        request,
        "reports/data_form.html",
        {"formset": formset, 'helper': helper },
    )