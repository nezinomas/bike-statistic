from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.template.loader import render_to_string
from django.urls import reverse_lazy

from ..core.mixins.views import (CreateViewMixin, DeleteViewMixin,
                                 DetailViewMixin, ListViewMixin,
                                 RedirectViewMixin, TemplateViewMixin,
                                 UpdateViewMixin)
from ..data.models import Data
from . import forms
from .lib.component_wear import ComponentWear
from .models import Bike, BikeInfo, Component, ComponentStatistic


# ---------------------------------------------------------------------------------------
#                                                                                   Bikes
# ---------------------------------------------------------------------------------------
class BikeDetail(DetailViewMixin):
    model = Bike
    template_name = 'bikes/includes/partial_bike_row.html'


class BikeList(ListViewMixin):
    def get_template_names(self):
        if self.request.htmx:
            return ['bikes/includes/partial_bike_list.html']
        return ['bikes/bike_list.html']

    def get_queryset(self):
        return Bike.objects.items()


class BikeCreate(CreateViewMixin):
    model = Bike
    form_class = forms.BikeForm
    template_name = 'bikes/bike_form.html'
    detail_view = BikeDetail

    def url(self):
        return reverse_lazy('bikes:bike_create')


class BikeUpdate(UpdateViewMixin):
    model = Bike
    form_class = forms.BikeForm
    template_name = 'bikes/bike_form.html'
    detail_view = BikeDetail

    def url(self):
        return reverse_lazy('bikes:bike_update', kwargs={'pk': self.kwargs['pk']})


class BikeDelete(DeleteViewMixin):
    model = Bike
    template_name = 'bikes/bike_confirm_delete.html'
    success_url = '/'


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


# ---------------------------------------------------------------------------------------
#                                                                              Components
# ---------------------------------------------------------------------------------------

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


class ComponentDetail(DetailViewMixin):
    model = Component
    template_name = 'bikes/includes/partial_component_row.html'


class ComponentList(ListViewMixin):
    def get_template_names(self):
        if self.request.htmx:
            return ['bikes/includes/partial_component_list.html']
        return ['bikes/component_list.html']

    def get_queryset(self):
        return Component.objects.items()


class ComponentCreate(CreateViewMixin):
    model = Component
    form_class = forms.ComponentForm
    template_name = 'bikes/component_form.html'
    detail_view = ComponentDetail

    def url(self):
        return reverse_lazy('bikes:component_create')


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
#                                                         Bike Component Statistic (Wear)
# ---------------------------------------------------------------------------------------
class StatsIndex(RedirectViewMixin):
    def get_redirect_url(self, *args, **kwargs):
        component = Component.objects.items()[:1]
        if not component.exists():
            return reverse('bikes:component_list')

        kwargs = {
            'bike_slug': self.kwargs['bike_slug'],
            'component_pk': component[0].pk,}
        return reverse('bikes:stats_list', kwargs=kwargs)


class StatsDetail(DetailViewMixin):
    model = ComponentStatistic
    lookup_url_kwarg = 'stats_pk'
    template_name = 'bikes/includes/partial_stats_row.html'


class StatsList(ListViewMixin):
    def get_template_names(self):
        if self.request.htmx:
            return ['bikes/includes/partial_stats_list.html']
        return ['bikes/stats_list.html']

    def get_queryset(self):
        return Component.objects.items()

    def get_context_data(self, **kwargs):
        bike = Bike.objects.related().get(slug=self.kwargs['bike_slug'])
        component = Component.objects.related().get(pk=self.kwargs['component_pk'])
        data = Data.objects.items().filter(bike=bike).values()
        component_statistic = \
            ComponentStatistic.objects \
            .items() \
            .filter(bike=bike, component=component)

        obj = ComponentWear(components=component_statistic, data=data)
        context = {
            'bike': bike,
            'component': component,
            'component_statistic': component_statistic,
            'km': obj.component_km,
            'stats': obj.component_stats,
            'total': obj.bike_km,
        }
        return super().get_context_data(**kwargs) | context


class StatsCreate(CreateViewMixin):
    model = ComponentStatistic
    template_name = 'bikes/stats_form.html'
    detail_view = StatsDetail

    def url(self):
        return reverse_lazy('bikes:stats_create', kwargs={'bike_slug': self.kwargs['bike_slug'], 'component_pk': self.kwargs['component_pk']})

    def get_form(self, data=None, files=None, **kwargs):
        # pass bike_slug and component_pk from self.kwargs to form
        return forms.ComponentStatisticForm(data, files, **kwargs | self.kwargs)


class StatsUpdate(UpdateViewMixin):
    model = ComponentStatistic
    form_class = forms.ComponentStatisticForm
    template_name = 'bikes/stats_form.html'
    lookup_url_kwarg = 'stats_pk'
    detail_view = StatsDetail

    def url(self):
        return reverse_lazy('bikes:stats_update', kwargs={'bike_slug': self.kwargs['bike_slug'], 'stats_pk': self.kwargs['stats_pk']})


class StatsDelete(DeleteViewMixin):
    model = ComponentStatistic
    template_name = 'bikes/stats_confirm_delete.html'
    lookup_url_kwarg = 'stats_pk'
    success_url = '/'
