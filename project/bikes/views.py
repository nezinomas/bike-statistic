from datetime import datetime
from django.db.models import Sum
from django.shortcuts import reverse
from django.urls import reverse_lazy

from ..core.mixins.views import (CreateViewMixin, DeleteViewMixin,
                                 DetailViewMixin, ListViewMixin,
                                 RedirectViewMixin, UpdateViewMixin)
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


# ---------------------------------------------------------------------------------------
#                                                                               Bike Info
# ---------------------------------------------------------------------------------------
class BikeInfoIndex(RedirectViewMixin):
    def get_redirect_url(self, *args, **kwargs):
        info = BikeInfo.objects.items()[:1]
        if not info.exists():
            return reverse('bikes:bike_list')

        return reverse('bikes:info_list', kwargs={'bike_slug': info[0].bike.slug})


class BikeInfoList(ListViewMixin):
    def get_template_names(self):
        if self.request.htmx:
            return ['bikes/includes/partial_info_list.html']
        return ['bikes/info_list.html']

    def get_queryset(self):
        return BikeInfo.objects.items().filter(bike__slug=self.kwargs['bike_slug'])


class BikeInfoDetail(DetailViewMixin):
    model = BikeInfo
    template_name = 'bikes/includes/partial_info_row.html'


class BikeInfoCreate(CreateViewMixin):
    model = BikeInfo
    template_name = 'bikes/info_form.html'
    detail_view = BikeInfoDetail

    def url(self):
        return reverse_lazy('bikes:info_create', kwargs={'bike_slug': self.kwargs['bike_slug']})

    def get_form(self, data=None, files=None, **kwargs):
        # pass bike_slug and component_pk from self.kwargs to form
        return forms.BikeInfoForm(data, files, **kwargs | self.kwargs)


class BikeInfoUpdate(UpdateViewMixin):
    model = BikeInfo
    form_class = forms.BikeInfoForm
    template_name = 'bikes/info_form.html'
    detail_view = BikeInfoDetail

    def url(self):
        return reverse_lazy('bikes:info_update', kwargs={'bike_slug': self.kwargs['bike_slug'], 'pk': self.kwargs['pk']})


class BikeInfoDelete(DeleteViewMixin):
    model = BikeInfo
    template_name = 'bikes/info_confirm_delete.html'
    success_url = '/'


# ---------------------------------------------------------------------------------------
#                                                                              Components
# ---------------------------------------------------------------------------------------
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


class ComponentUpdate(UpdateViewMixin):
    model = Component
    form_class = forms.ComponentForm
    template_name = 'bikes/component_form.html'
    detail_view = ComponentDetail

    def url(self):
        return reverse_lazy('bikes:component_update', kwargs={'pk': self.kwargs['pk']})


class ComponentDelete(DeleteViewMixin):
    model = Component
    template_name = 'bikes/component_confirm_delete.html'
    success_url = '/'


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

    def get_context_data(self, **kwargs):
        bike_slug = self.kwargs['bike_slug']
        stats_pk = self.kwargs['stats_pk']
        start_date = self.object.start_date
        end_date = self.object.end_date or datetime.now().date

        distance_sum = Data.objects \
            .filter(
                bike__slug=bike_slug,
                date__range=(start_date, end_date)) \
            .aggregate(Sum('distance'))

        context = {
            'km': {str(stats_pk): distance_sum.get('distance__sum', 0)},}

        return super().get_context_data(**kwargs) | context

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
        data = Data.objects.items().filter(bike=bike).values('date', 'distance')

        component_statistic = \
            ComponentStatistic.objects \
            .items() \
            .filter(bike=bike, component=component)

        obj = ComponentWear(
            [*component_statistic.values('start_date', 'end_date', 'pk')], [*data])
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
    hx_trigger_django = 'reload'

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
    hx_trigger_django = 'reload'

    def url(self):
        return reverse_lazy('bikes:stats_update', kwargs={'bike_slug': self.kwargs['bike_slug'], 'stats_pk': self.kwargs['stats_pk']})


class StatsDelete(DeleteViewMixin):
    model = ComponentStatistic
    template_name = 'bikes/stats_confirm_delete.html'
    lookup_url_kwarg = 'stats_pk'
    success_url = '/'
    hx_trigger_django = 'reload'
