from django.shortcuts import reverse, render, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse

from .models import Bike, Component, ComponentStatistic
from .forms import ComponentForm


def index(request):
    return render(
        request,
        'bikes/index.html',
        context={'var': 'kintamasis is view', 'var1': '? ar tikrai?'}
    )


def save_component(request, context, form, template_name):
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
        template_name=template_name,
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
    return save_component(request, context, form, 'bikes/includes/partial_component_update.html')


def component_update(request, pk):
    component = get_object_or_404(Component, pk=pk)
    form = ComponentForm(request.POST or None, instance=component)
    context = {'url': reverse('bikes:component_update', kwargs={'pk': pk})}
    return save_component(request, context, form, 'bikes/includes/partial_component_update.html')


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


def bike_component_list(request, bike):
    bike_ = get_object_or_404(Bike, slug__iexact=bike)

    return render(request, 'bikes/bike_component_list.html', {'obj': bike_})

