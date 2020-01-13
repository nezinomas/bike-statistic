from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.template.loader import render_to_string

from ...reports.models import Data
from ..forms import ComponentStatisticForm
from ..lib.component_wear import ComponentWear
from ..models import Bike, Component, ComponentStatistic


def form_valid(data, bike_slug, component_pk):
    components = Component.objects.items()
    data1 = (
        Data.objects
        .items()
        .filter(bike__slug=bike_slug)
        .values()
    )
    component_statistic = (
        ComponentStatistic.objects
        .items()
        .filter(bike__slug=bike_slug, component__pk=component_pk)
        .values()
    )

    obj = ComponentWear(components=component_statistic, data=data1)

    data['form_is_valid'] = True
    data['html_list'] = render_to_string(
        'bikes/includes/partial_stats_list.html',
        {
            'components': components,
            'component_statistic': component_statistic,
            'km': obj.component_km,
            'stats': obj.component_stats,
            'total': obj.bike_km,
            'bike_slug': bike_slug,
        }
    )


def save_data(request, context, form, bike_slug, pk):
    data = {}

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            form_valid(data, bike_slug, pk)
        else:
            data['form_is_valid'] = False

    context['form'] = form
    data['html_form'] = render_to_string(
        template_name='bikes/includes/partial_stats_update.html',
        context=context,
        request=request
    )
    return JsonResponse(data)


@login_required()
def index(request, bike_slug):
    qs = Component.objects.items().first()
    url = reverse(
        'bikes:stats_list',
        kwargs={'bike_slug': bike_slug, 'component_pk': qs.pk}
    )
    return redirect(url)


@login_required()
def lists(request, bike_slug, component_pk):
    component = Component.objects.get(pk=component_pk)
    components = Component.objects.items()
    data = (
        Data.objects
        .items()
        .filter(bike__slug=bike_slug)
        .values()
    )
    component_statistic = (
        ComponentStatistic.objects
        .items()
        .filter(bike__slug=bike_slug, component__pk=component_pk)
        .values()
    )

    obj = ComponentWear(components=component_statistic, data=data)

    return render(
        request,
        'bikes/stats_list.html', {
            'component': component,
            'components': components,
            'component_statistic': component_statistic,
            'km': obj.component_km,
            'stats': obj.component_stats,
            'total': obj.bike_km,
            'bike_slug': bike_slug,
        }
    )


@login_required()
def create(request, bike_slug, component_pk):
    bike_object = get_object_or_404(Bike, slug=bike_slug)
    component_object = get_object_or_404(Component, pk=component_pk)

    form = ComponentStatisticForm(
        request.POST or None,
        initial={'bike': bike_object, 'component': component_object}
    )
    url = reverse(
        'bikes:stats_create',
        kwargs={'bike_slug': bike_slug, 'component_pk': component_pk}
    )
    context = {'url': url}
    return save_data(request, context, form, bike_slug, component_pk)


@login_required()
def update(request, bike_slug, stats_pk):
    obj = get_object_or_404(ComponentStatistic, pk=stats_pk)
    form = ComponentStatisticForm(request.POST or None, instance=obj)
    url = reverse(
        'bikes:stats_update',
        kwargs={'bike_slug': bike_slug, 'stats_pk': stats_pk}
    )
    context = {'url': url}
    return save_data(request, context, form, bike_slug, obj.component.pk)


@login_required()
def delete(request, bike_slug, stats_pk):
    obj = get_object_or_404(ComponentStatistic, pk=stats_pk)
    data = {}
    if request.method == 'POST':
        obj.delete()
        form_valid(data, bike_slug, obj.component.pk)
    else:
        context = {'component': obj, 'bike_slug': bike_slug}
        data['html_form'] = render_to_string(
            'bikes/includes/partial_stats_delete.html',
            context,
            request
        )
    return JsonResponse(data)
