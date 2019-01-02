from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse

from .models import Component, ComponentStatistic
from .forms import ComponentForm


def index(request):
    return render(
        request,
        'bikes/index.html',
        context={'var': 'kintamasis is view', 'var1': '? ar tikrai?'}
    )


def save_component(request, form, template_name):
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

    context = {'form': form}
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
    if request.method == 'POST':
        form = ComponentForm(request.POST)
    else:
        form = ComponentForm()

    return save_component(request, form, 'bikes/includes/partial_component_create.html')


def component_update(request, pk):
    component = get_object_or_404(Component, pk=pk)
    if request.method == 'POST':
        form = ComponentForm(request.POST, instance=component)
    else:
        form = ComponentForm(instance=component)

    return save_component(request, form, 'bikes/includes/partial_component_update.html')


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

