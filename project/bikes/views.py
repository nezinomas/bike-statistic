from django.shortcuts import reverse, render, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse

from .models import Bike, Component, ComponentStatistic
from .forms import ComponentForm, ComponentStatisticForm

from ..reports.models import Data

from .helpers.view_stats_helper import Filter


def index(request):
    return render(
        request,
        'bikes/index.html',
        context={'var': 'kintamasis is view', 'var1': '? ar tikrai?'}
    )


def save_component(request, context, form):
    data = {}

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            components = Component.objects.all()
            data['html_list'] = render_to_string(
                'bikes/includes/partial_component_list.html', {'components': components})
        else:
            data['form_is_valid'] = False

    context['form'] = form
    data['html_form'] = render_to_string(
        template_name='bikes/includes/partial_component_update.html',
        context=context,
        request=request
    )

    return JsonResponse(data)


def save_component1(request, context, form, bike_slug, pk):
    data = {}

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True

            o = Filter(bike_slug, pk)
            data['html_list'] = render_to_string(
                'bikes/includes/partial_stats_list.html',
                {'components': o.components(), 'total': o.total_distance(), 'bike_slug': bike_slug}
            )
        else:
            data['form_is_valid'] = False

    context['form'] = form
    data['html_form'] = render_to_string(
        template_name='bikes/includes/partial_stats_update.html',
        context=context,
        request=request
    )

    return JsonResponse(data)


def component_list(request):
    components = Component.objects.all()
    return render(request, 'bikes/component_list.html', {'components': components})


def component_create(request):
    form = ComponentForm(request.POST or None)
    context = {'url': reverse('bikes:component_create')}
    return save_component(request, context, form)


def component_update(request, pk):
    component = get_object_or_404(Component, pk=pk)
    form = ComponentForm(request.POST or None, instance=component)
    context = {'url': reverse('bikes:component_update', kwargs={'pk': pk})}
    return save_component(request, context, form)


def component_delete(request, pk):
    component = get_object_or_404(Component, pk=pk)
    data = {}

    if request.method == 'POST':
        component.delete()
        data['form_is_valid'] = True
        components = Component.objects.all()
        data['html_list'] = render_to_string('bikes/includes/partial_component_list.html', {'components': components})
    else:
        context = {'component':component}
        data['html_form'] = render_to_string('bikes/includes/partial_component_delete.html', context=context, request=request)

    return JsonResponse(data)


def stats_list(request, bike):
    o = Filter(bike, 'all')

    return render(
        request,
        'bikes/stats_list.html', {
            'components': o.components(),
            'total': o.total_distance(),
            'bike_slug': bike
        })


def stats_create(request, bike, pk):
    bike_ = get_object_or_404(Bike, slug=bike)
    obj = get_object_or_404(Component, pk=pk)

    form = ComponentStatisticForm(
        request.POST or None,
        initial={'bike': bike_, 'component': component_}
    )
    context = {
        'url': reverse('bikes:stats_create', kwargs={'bike': bike, 'pk': pk}),
        'tbl': pk
    }
    return save_component1(request, context, form, bike, pk)


def stats_update(request, bike, pk):
    obj = get_object_or_404(ComponentStatistic, pk=pk)
    form = ComponentStatisticForm(request.POST or None, instance=obj)
    context = {
        'url': reverse('bikes:stats_update', kwargs={'bike': bike, 'pk': pk}),
        'tbl': obj.component.pk
    }
    return save_component1(request, context, form, bike, obj.component.pk)


def stats_delete(request, bike, pk):
    obj = get_object_or_404(ComponentStatistic, pk=pk)
    data = {}
    if request.method == 'POST':
        obj.delete()
        data['form_is_valid'] = True

        o = Filter(bike, obj.component.pk)
        data['html_list'] = render_to_string(
            'bikes/includes/partial_stats_list.html',
            {'components': o.components(), 'total': o.total_distance(), 'bike_slug': bike}
        )

    else:
        context = {'component': obj, 'bike_slug': bike}
        data['html_form'] = render_to_string(
            'bikes/includes/partial_stats_delete.html', context=context, request=request)

    return JsonResponse(data)
