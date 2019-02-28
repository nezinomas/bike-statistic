from django.shortcuts import reverse, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse

from ..models import Component
from ..forms import ComponentForm


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


@login_required()
def lists(request):
    components = Component.objects.all()
    return render(request, 'bikes/component_list.html', {'components': components})


@login_required()
def create(request):
    form = ComponentForm(request.POST or None)
    context = {'url': reverse('bikes:component_create')}
    return save_component(request, context, form)


@login_required()
def update(request, pk):
    component = get_object_or_404(Component, pk=pk)
    form = ComponentForm(request.POST or None, instance=component)
    context = {'url': reverse('bikes:component_update', kwargs={'pk': pk})}
    return save_component(request, context, form)


@login_required()
def delete(request, pk):
    component = get_object_or_404(Component, pk=pk)
    data = {}

    if request.method == 'POST':
        component.delete()
        data['form_is_valid'] = True
        components = Component.objects.all()
        data['html_list'] = render_to_string(
            'bikes/includes/partial_component_list.html',
            {'components': components}
        )
    else:
        context = {'component': component}
        data['html_form'] = render_to_string(
            'bikes/includes/partial_component_delete.html',
            context=context,
            request=request
        )
    return JsonResponse(data)
