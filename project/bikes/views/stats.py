from django.shortcuts import reverse, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse

from ..models import Bike, Component, ComponentStatistic
from ..forms import ComponentStatisticForm

from ..helpers.view_stats_helper import Filter


def form_valid(data, bike_slug, pk):
    obj = Filter(bike_slug, pk)
    data['form_is_valid'] = True
    data['html_list'] = render_to_string(
        'bikes/includes/partial_stats_list.html',
        {
            'components': obj.components(),
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
def stats_list(request, bike):
    o = Filter(bike, 'all')

    return render(
        request,
        'bikes/stats_list.html', {
            'components': o.components(),
            'total': o.total_distance(),
            'bike_slug': bike
        }
    )


@login_required()
def stats_create(request, bike, pk):
    bike_object = get_object_or_404(Bike, slug=bike)
    component_object = get_object_or_404(Component, pk=pk)

    form = ComponentStatisticForm(
        request.POST or None,
        initial={'bike': bike_object, 'component': component_object}
    )
    context = {
        'url': reverse('bikes:stats_create', kwargs={'bike': bike, 'pk': pk}),
        'tbl': pk
    }
    return save_data(request, context, form, bike, pk)


@login_required()
def stats_update(request, bike, pk):
    obj = get_object_or_404(ComponentStatistic, pk=pk)
    form = ComponentStatisticForm(request.POST or None, instance=obj)
    context = {
        'url': reverse('bikes:stats_update', kwargs={'bike': bike, 'pk': pk}),
        'tbl': obj.component.pk
    }
    return save_data(request, context, form, bike, obj.component.pk)


@login_required()
def stats_delete(request, bike, pk):
    obj = get_object_or_404(ComponentStatistic, pk=pk)
    data = {}
    if request.method == 'POST':
        obj.delete()
        form_valid(data, bike, obj.component.pk)
    else:
        context = {'component': obj, 'bike_slug': bike}
        data['html_form'] = render_to_string(
            'bikes/includes/partial_stats_delete.html',
            context,
            request
        )
    return JsonResponse(data)
