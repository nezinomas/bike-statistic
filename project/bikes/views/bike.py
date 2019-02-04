from django.shortcuts import reverse, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse

from ..models import Bike
from ..forms import BikeForm


def form_valid(data):
    objects = Bike.objects.all()
    data['form_is_valid'] = True
    data['html_list'] = render_to_string(
        'bikes/includes/partial_bike_list.html',
        {'objects': objects}
    )


def save_data(request, context, form):
    data = {}

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            form_valid(data)
        else:
            data['form_is_valid'] = False

    context['form'] = form
    data['html_form'] = render_to_string(
        template_name='bikes/includes/partial_bike_update.html',
        context=context,
        request=request
    )
    return JsonResponse(data)


@login_required()
def lists(request):
    obj = Bike.objects.all()
    # reikia, nes kitaip pirma karta paspaudus ant date picker jis neveikia
    form_media = BikeForm(None).media
    rendered = render(
        request,
        'bikes/bike_list.html',
        {'objects': obj, 'form_media': form_media}
    )
    return rendered


@login_required()
def create(request):
    form = BikeForm(request.POST or None)
    context = {'url': reverse('bikes:bike_create')}
    return save_data(request, context, form)


@login_required()
def update(request, pk):
    obj = get_object_or_404(Bike, pk=pk)
    form = BikeForm(request.POST or None, instance=obj)
    url = reverse('bikes:bike_update', kwargs={'pk': pk})
    context = {'url': url}
    return save_data(request, context, form)


@login_required()
def delete(request, pk):
    obj = get_object_or_404(Bike, pk=pk)
    data = {}

    if request.method == 'POST':
        obj.delete()
        form_valid(data)
    else:
        context = {'object': obj}
        data['html_form'] = render_to_string(
            'bikes/includes/partial_bike_delete.html',
            context,
            request
        )
    return JsonResponse(data)
