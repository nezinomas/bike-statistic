from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.template.loader import render_to_string

from ..forms import ComponentStatisticForm
from ..helpers.view_stats_helper import Filter
from ..models import Bike, Component, ComponentStatistic


def form_valid(data, bike_slug, pk):
    obj = Filter(bike_slug, pk)
    data['form_is_valid'] = True
    data['html_list'] = render_to_string(
        'bikes/includes/partial_stats_list.html',
        {
            'components_list': obj.components_list,
            'components_stats': obj.components_stats,
            'total': obj.total_distance(),
            'bike_slug': bike_slug
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
    qs = Component.objects.all().first()
    url = reverse(
        'bikes:stats_list',
        kwargs={'bike_slug': bike_slug, 'component_pk': qs.pk}
    )
    return redirect(url)


@login_required()
def lists(request, bike_slug, component_pk):
    o = Filter(bike_slug, component_pk)

    return render(
        request,
        'bikes/stats_list.html', {
            'components_list': o.components_list,
            'components_stats': o.components_stats,
            'total': o.total_distance(),
            'bike_slug': bike_slug,
            'component_pk': component_pk,
            'component_name': o.component.name
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
