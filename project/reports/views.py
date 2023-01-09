from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy

from ..bikes.models import Bike
from ..core.lib import utils
from ..goals.models import Goal
from . import forms, models
from .helpers import view_data_helper as helper
from .library.chart import get_color
from .library.distance_summary import DistanceSummary
from .library.insert_garmin import SyncWithGarmin
from .library.progress import Progress


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

    objects = (
        models.Data.objects.items()
        .filter(date__range=(start_date, end_date))
    )
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
    obj = get_object_or_404(models.Data, pk=pk)
    data = {}

    if request.method == 'POST':
        obj.delete()
        helper.form_valid(data, start_date, end_date)
    else:
        context = {'object': obj, 'start_date': start_date, 'end_date': end_date}
        data['html_form'] = render_to_string(
            'reports/includes/partial_data_delete.html', context, request)

    return JsonResponse(data)


@login_required()
def data_update(request, start_date, end_date, pk):
    obj = get_object_or_404(models.Data, pk=pk)
    form = forms.DataForm(request.POST or None, instance=obj)
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
    obj = get_object_or_404(models.Data, pk=pk)
    obj.checked = 'y'
    obj.save()

    objects = (
        models.Data.objects.items()
        .filter(date__range=(start_date, end_date))
    )

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
        SyncWithGarmin().insert_data_current_user()
        msg = '<p>OK</p>'
    except Exception as ex:
        msg = (
            f'<p>{ex}</p>'
            f'<p>{"-"*120}</p>'
            f'<p>Type: {type(ex).__name__}</p>'
            f'<p>Args: {ex.args}</p>'
        )
        return render(
            request,
            template_name='reports/data_insert.html',
            context={'message': msg}
        )
    return redirect(reverse('reports:data_empty'))

@login_required()
def table(request, year):
    goal = list(
        Goal.objects
        .items()
        .filter(year=year)
        .values_list('goal', flat=True)
    )
    goal = goal[0] if goal else 0

    obj = Progress(year)

    return render(
        request,
        'reports/table.html',
        {
            'year': year,
            'e': obj.extremums().get(year),
            'season': obj.season_progress(goal=goal),
            'month': obj.month_stats(),
        }
    )


def overall(request):
    years = utils.years()
    bikes = Bike.objects.items().values_list(
        'short_name', flat=True).order_by('date')
    data = models.Data.objects.bike_summary()

    obj = DistanceSummary(years=years, bikes=bikes, data=data)

    # update chart_data with bar color, border color, border_width
    chart_data = obj.chart_data
    for i, dt in enumerate(chart_data):
        dt.update({
            'color': get_color(i, 0.35),
            'borderColor': get_color(i, 1),
            'borderWidth': '0.5',
        })

    context = {
        'year_list': years,
        'chart_data': chart_data[::-1],
        'bikes': bikes,
        'table_data': list(zip(obj.table, obj.total_column)),
        'total_row': obj.total_row,
        'total': sum(obj.total_row.values())
    }
    return render(request, template_name='reports/overall.html', context=context)
