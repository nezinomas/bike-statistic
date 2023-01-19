from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.template.loader import render_to_string

from ..core.mixins.views import (CreateViewMixin, DeleteViewMixin,
                                 DetailViewMixin, ListViewMixin,
                                 RedirectViewMixin, TemplateViewMixin,
                                 UpdateViewMixin)
from ..data.models import Data
from .forms import (BikeForm, BikeInfoForm, ComponentForm,
                    ComponentStatisticForm)
from .lib.component_wear import ComponentWear
from .models import Bike, BikeInfo, Component, ComponentStatistic


def form_valid1(data):
    objects = Bike.objects.items()
    data['form_is_valid'] = True
    data['html_list'] = render_to_string(
        'bikes/includes/partial_bike_list.html',
        {'objects': objects}
    )


def bike_save_data(request, context, form):
    data = {}

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            form_valid1(data)
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
def bike_lists(request):
    obj = Bike.objects.items()
    # reikia, nes kitaip pirma karta paspaudus ant date picker jis neveikia
    form_media = BikeForm(None).media
    rendered = render(
        request,
        'bikes/bike_list.html',
        {'objects': obj, 'form_media': form_media}
    )
    return rendered


@login_required()
def bike_create(request):
    form = BikeForm(request.POST or None)
    context = {'url': reverse('bikes:bike_create')}
    return bike_save_data(request, context, form)


@login_required()
def bike_update(request, pk):
    obj = get_object_or_404(Bike, pk=pk)
    form = BikeForm(request.POST or None, instance=obj)
    url = reverse('bikes:bike_update', kwargs={'pk': pk})
    context = {'url': url}
    return bike_save_data(request, context, form)


@login_required()
def bike_delete(request, pk):
    obj = get_object_or_404(Bike, pk=pk)
    data = {}

    if request.method == 'POST':
        obj.delete()
        form_valid1(data)
    else:
        context = {'object': obj}
        data['html_form'] = render_to_string(
            'bikes/includes/partial_bike_delete.html',
            context,
            request
        )
    return JsonResponse(data)


# ----------------------------------------------------------------------------- Bike Info
def form_valid2(data, bike_slug):
    objects = BikeInfo.objects.items().filter(bike__slug=bike_slug)
    data['form_is_valid'] = True
    data['html_list'] = render_to_string(
        'bikes/includes/partial_info_list.html',
        {'objects': objects, 'bike_slug': bike_slug}
    )


def bike_info_save_data(request, context, form, bike_slug):
    data = {}

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            form_valid2(data, bike_slug)
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
def bike_info_index(request):
    bike = Bike.objects.items().first()

    bike_slug = 'no_bike'
    if bike:
        bike_slug = bike.slug

    return redirect(reverse('bikes:info_list', kwargs={'bike_slug': bike_slug}))


@login_required()
def bike_info_lists(request, bike_slug):
    obj = BikeInfo.objects.items().filter(bike__slug=bike_slug)
    rendered = render(
        request,
        'bikes/info_list.html',
        {'objects': obj, 'bike_slug': bike_slug}
    )
    return rendered


@login_required()
def bike_info_create(request, bike_slug):
    bike = get_object_or_404(Bike, slug=bike_slug)
    form = BikeInfoForm(request.POST or None, initial={'bike': bike})
    context = {'url': reverse('bikes:info_create', kwargs={
                              'bike_slug': bike_slug})}

    return bike_info_save_data(request, context, form, bike_slug)


@login_required()
def bike_info_update(request, bike_slug, pk):
    obj = get_object_or_404(BikeInfo, pk=pk)
    form = BikeInfoForm(request.POST or None, instance=obj)
    context = {
        'url': reverse('bikes:info_update', kwargs={'bike_slug': bike_slug, 'pk': pk})
    }
    return bike_info_save_data(request, context, form, bike_slug)


@login_required()
def bike_info_delete(request, bike_slug, pk):
    obj = get_object_or_404(BikeInfo, pk=pk)
    data = {}
    if request.method == 'POST':
        obj.delete()
        form_valid2(data, bike_slug)
    else:
        context = {'object': obj, 'bike_slug': bike_slug}
        data['html_form'] = render_to_string(
            'bikes/includes/partial_info_delete.html',
            context,
            request
        )
    return JsonResponse(data)


# ------------------------------------------------------------------------ Bike Component

def save_component(request, context, form):
    data = {}

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            components = Component.objects.items()
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
def component_lists(request):
    components = Component.objects.items()
    return render(
        request,
        'bikes/component_list.html',
        {'components': components}
    )


@login_required()
def component_create(request):
    form = ComponentForm(request.POST or None)
    context = {'url': reverse('bikes:component_create')}
    return save_component(request, context, form)


@login_required()
def component_update(request, pk):
    component = get_object_or_404(Component, pk=pk)
    form = ComponentForm(request.POST or None, instance=component)
    context = {'url': reverse('bikes:component_update', kwargs={'pk': pk})}
    return save_component(request, context, form)


@login_required()
def component_delete(request, pk):
    component = get_object_or_404(Component, pk=pk)
    data = {}

    if request.method == 'POST':
        component.delete()
        data['form_is_valid'] = True
        components = Component.objects.items()
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


# ---------------------------------------------------------------------------------------
#                                                                          Component Wear
# ---------------------------------------------------------------------------------------
def bike_stats_form_valid(data, bike_slug, component_pk):
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


def bike_stats_save_data(request, context, form, bike_slug, pk):
    data = {}

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            bike_stats_form_valid(data, bike_slug, pk)
        else:
            data['form_is_valid'] = False

    context['form'] = form
    data['html_form'] = render_to_string(
        template_name='bikes/includes/partial_stats_update.html',
        context=context,
        request=request
    )
    return JsonResponse(data)


class ComponentWearIndex(RedirectViewMixin):
    def get_redirect_url(self, *args, **kwargs):
        try:
            component = Component.objects.items().first()
        except Component.DoesNotExist:
            return reverse('bikes:component_list')
        else:
            bike_slug = self.kwargs['bike_slug']
            return reverse(
                'bikes:stats_list',
                kwargs={'bike_slug': bike_slug, 'component_pk': component.pk})


class ComponentWearDetail(DetailViewMixin):
    model = ComponentStatistic
    template_name = 'data/includes/partial_component_wear_row.html'


class ComponentWearList(ListViewMixin):
    def get_template_names(self):
        if self.request.htmx:
            return ['bikes/includes/partial_component_wear_list.html']
        return ['bikes/component_wear_list.html']

    def get_queryset(self):
        return Component.objects.items()

    def get_context_data(self, **kwargs):
        bike_slug = self.kwargs['bike_slug']
        component = Component.objects.get(pk=self.kwargs['component_pk'])
        data = (
            Data.objects
            .items()
            .filter(bike__slug=bike_slug)
            .values()
        )
        component_statistic = (
            ComponentStatistic.objects
            .items()
            .filter(bike__slug=bike_slug, component__pk=component.pk)
            .values()
        )
        obj = ComponentWear(components=component_statistic, data=data)
        context = {
            'component': component,
            'component_statistic': component_statistic,
            'km': obj.component_km,
            'stats': obj.component_stats,
            'total': obj.bike_km,
            'bike_slug': bike_slug,
        }
        return super().get_context_data(**kwargs) | context


class StatsCreate(CreateViewMixin):
    model = ComponentStatistic
    template_name = 'bikes/stats_form.html'
    detail_template_name = 'bikes/includes/partial_stats_row.html'

    def url(self):
        return reverse_lazy('bikes:stats_create', kwargs={'bike_slug': self.kwargs['bike_slug'], 'component_pk': self.kwargs['component_pk']})

    def get_form(self, data=None, files=None, **kwargs):
        # pass bike_slug and component_pk from self.kwargs to form
        return ComponentStatisticForm(data, files, **kwargs | self.kwargs)


@login_required()
def bike_stats_update(request, bike_slug, stats_pk):
    obj = get_object_or_404(ComponentStatistic, pk=stats_pk)
    form = ComponentStatisticForm(request.POST or None, instance=obj)
    url = reverse(
        'bikes:stats_update',
        kwargs={'bike_slug': bike_slug, 'stats_pk': stats_pk}
    )
    context = {'url': url}
    return bike_stats_save_data(request, context, form, bike_slug, obj.component.pk)


@login_required()
def bike_stats_delete(request, bike_slug, stats_pk):
    obj = get_object_or_404(ComponentStatistic, pk=stats_pk)
    data = {}
    if request.method == 'POST':
        obj.delete()
        bike_stats_form_valid(data, bike_slug, obj.component.pk)
    else:
        context = {'component': obj, 'bike_slug': bike_slug}
        data['html_form'] = render_to_string(
            'bikes/includes/partial_stats_delete.html',
            context,
            request
        )
    return JsonResponse(data)
