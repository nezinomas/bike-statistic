from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.template.loader import render_to_string

from ..forms import BikeInfoForm
from ..models import Bike, BikeInfo


def form_valid(data, bike_slug):
    objects = BikeInfo.objects.\
        prefetch_related('bike').\
        filter(bike__slug=bike_slug)
    data['form_is_valid'] = True
    data['html_list'] = render_to_string(
        'bikes/includes/partial_info_list.html',
        {'objects': objects, 'bike_slug': bike_slug}
    )


def save_data(request, context, form, bike_slug):
    data = {}

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            form_valid(data, bike_slug)
        else:
            data['form_is_valid'] = False

    context['form'] = form
    data['html_form'] = render_to_string(
        template_name='bikes/includes/partial_info_update.html',
        context=context,
        request=request
    )
    return JsonResponse(data)


@login_required()
def index(request):
    bike = Bike.objects.prefetch_related('bike').all().first()
    return redirect(reverse('bikes:info_list', kwargs={'bike_slug': bike.slug}))


@login_required()
def lists(request, bike_slug):
    obj = BikeInfo.objects.prefetch_related('bike').filter(bike__slug=bike_slug)
    rendered = render(
        request,
        'bikes/info_list.html',
        {'objects': obj, 'bike_slug': bike_slug}
    )
    return rendered


@login_required()
def create(request, bike_slug):
    bike = get_object_or_404(Bike, slug=bike_slug)
    form = BikeInfoForm(request.POST or None, initial={'bike': bike})
    context = {'url': reverse('bikes:info_create', kwargs={'bike_slug': bike_slug})}

    return save_data(request, context, form, bike_slug)


@login_required()
def update(request, bike_slug, pk):
    obj = get_object_or_404(BikeInfo, pk=pk)
    form = BikeInfoForm(request.POST or None, instance=obj)
    context = {
        'url': reverse('bikes:info_update', kwargs={'bike_slug': bike_slug, 'pk': pk})
    }
    return save_data(request, context, form, bike_slug)


@login_required()
def delete(request, bike_slug, pk):
    obj = get_object_or_404(BikeInfo, pk=pk)
    data = {}
    if request.method == 'POST':
        obj.delete()
        form_valid(data, bike_slug)
    else:
        context = {'object': obj, 'bike_slug': bike_slug}
        data['html_form'] = render_to_string(
            'bikes/includes/partial_info_delete.html',
            context,
            request
        )
    return JsonResponse(data)
