from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy

from . import forms, models

from .library.insert_data import insert_data as inserter
from .library.overall import Overall
from .helpers import view_data_helper as helper


@login_required()
def index(request):
    return redirect(reverse('reports:data_empty'))


@login_required()
def data_empty(request):
    return redirect(
        reverse(
            'reports:data_list',
            kwargs={
                'start_date': helper.format_date(),
                'end_date': helper.format_date('last'),
            }
        )
    )


@login_required()
def data_partial(request, start_date):
    return redirect(
        reverse(
            'reports:data_list',
            kwargs={
                'start_date': start_date,
                'end_date': helper.format_date('last'),
            }
        )
    )


@login_required()
def data_list(request, start_date, end_date):
    # paspaustas filter mygtukas
    if 'date_filter' in request.POST:
        filter_form = forms.DateFilterForm(request.POST)

        if filter_form.is_valid():
            data = filter_form.cleaned_data
            kwargs = {'start_date': data['start_date'], 'end_date': data['end_date']}
            url = reverse_lazy('reports:data_list', kwargs=kwargs)
            return redirect(url)

    objects = models.Data.objects\
        .prefetch_related('bike')\
        .filter(date__range=(start_date, end_date))
    filter_form = forms.DateFilterForm(
        initial={'start_date': start_date, 'end_date': end_date}
    )
    context = {
        'objects': objects,
        'filter_form': filter_form,
        'start_date': start_date,
        'end_date': end_date
    }
    return render(request, 'reports/data_list.html', context)


@login_required()
def data_create(request, start_date, end_date):
    form = forms.DataForm(request.POST or None)
    url = reverse(
        'reports:data_create',
        kwargs={'start_date': start_date, 'end_date': end_date}
    )
    context = {'url': url}
    return helper.save_data(request, context, form, start_date, end_date)


@login_required
def data_delete(request, start_date, end_date, pk):
    object = get_object_or_404(models.Data, pk=pk)
    data = {}

    if request.method == 'POST':
        object.delete()
        helper.form_valid(data, start_date, end_date)
    else:
        context = {'object': object, 'start_date': start_date, 'end_date': end_date}
        data['html_form'] = render_to_string(
            'reports/includes/partial_data_delete.html', context, request)

    return JsonResponse(data)


@login_required()
def data_update(request, start_date, end_date, pk):
    object = get_object_or_404(models.Data, pk=pk)
    form = forms.DataForm(request.POST or None, instance=object)
    url = reverse(
        'reports:data_update',
        kwargs={
            'start_date': start_date,
            'end_date': end_date,
            'pk': pk
        }
    )
    context = {'url': url}
    return helper.save_data(request, context, form, start_date, end_date)


@login_required()
def data_quick_update(request, start_date, end_date, pk):
    object = get_object_or_404(models.Data, pk=pk)
    object.checked = 'y'
    object.save()

    objects = models.Data.objects\
        .prefetch_related('bike')\
        .filter(date__range=(start_date, end_date))

    context = {
        'objects': objects,
        'start_date': start_date,
        'end_date': end_date
    }

    data = {
        'html_list': render_to_string(
            'reports/includes/partial_data_list.html',
            context=context,
            request=request,
        )
    }
    return JsonResponse(data)

@login_required()
def insert_data(request):
    try:
        inserter(10)
        message = 'ok'
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        return render(
            request,
            template_name='reports/data_insert.html',
            context={'message': message}
        )
    return redirect(reverse('reports:data_empty'))


def api_overall(request):
    obj = Overall(models.Data)
    chart = {
        'first': {
            'xAxis': {'categories': obj.create_categories()},
            'series': obj.create_series()[::-1]
        }
    }
    return JsonResponse(chart)


def overall(request):
    return render(request, template_name='reports/overall.html', context={})
