from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy

from ..bikes.models import Bike
from ..core.lib import utils
from ..core.mixins.views import (CreateViewMixin, DeleteViewMixin,
                                 DetailViewMixin, ListViewMixin,
                                 TemplateViewMixin, UpdateViewMixin)
from . import forms, models
from .helpers import view_data_helper as helper
from .library.chart import get_color
from .library.distance_summary import DistanceSummary
from .library.insert_garmin import SyncWithGarmin
from .library.progress import Progress, ProgressData


class DataList(ListViewMixin):
    model = models.Data

    def get_queryset(self):
        start_date = self.request.GET.get('start_date') or helper.format_date(day=1)
        end_date = self.request.GET.get('end_date') or helper.format_date()
        return self.model.objects.items().filter(date__range=(start_date, end_date))

    def get_template_names(self):
        if self.request.htmx:
            return ['reports/includes/partial_data_list.html']
        return ['reports/data_list.html']

    def get_context_data(self, **kwargs):
        context = {
            'filter_form': forms.DateFilterForm(self.request.GET or None),
        }
        return super().get_context_data(**kwargs) | context


class YearProgress(TemplateViewMixin):
    template_name = 'reports/table.html'

    def get_context_data(self, **kwargs):
        year = self.kwargs.get('year')
        data = ProgressData(year)
        obj = Progress(data)
        context = {
            'year': year,
            'e': obj.extremums().get(year),
            'season': obj.season_progress(),
            'month': obj.month_stats(),
        }
        return super().get_context_data(**kwargs) | context


class DataDetail(DetailViewMixin):
    model = models.Data
    template_name = 'reports/includes/partial_data_row.html'


class QuickUpdate(DetailViewMixin):
    model = models.Data
    template_name = 'reports/includes/partial_data_row.html'

    def get_context_data(self, **kwargs):
        self.object.checked = 'y'
        self.object.save()
        context = {'obj': self.object}
        return super().get_context_data(**kwargs) | context


class DataCreate(CreateViewMixin):
    model = models.Data
    form_class = forms.DataForm
    success_url = reverse_lazy('reports:index')
    hx_trigger_django = 'reload'

    def url(self):
        return reverse_lazy('reports:data_create')


class DataDelete(DeleteViewMixin):
    model = models.Data
    success_url = reverse_lazy('reports:index')
    hx_trigger_django = 'reload'


class DataUpdate(UpdateViewMixin):
    model = models.Data
    form_class = forms.DataForm
    hx_trigger_django = 'reload_after_object_update'

    def get_success_url(self):
        return reverse_lazy('reports:data_update', kwargs={'pk': self.object.pk})

    def url(self):
        return self.get_success_url()


@login_required()
def insert_data(request):
    try:
        SyncWithGarmin().insert_data_current_user()
    except Exception as ex:
        msg = (
            f'<p>{ex}</p>'
            f'<p>{"-"*120}</p>'
            f'<p>Type: {type(ex).__name__}</p>'
            f'<p>Args: {ex.args}</p>'
        )
        return render(
            request,
            template_name='reports/data_insert.html',
            context={'message': msg}
        )
    return redirect(reverse('reports:index'))


def overall(request):
    years = utils.years()
    bikes = Bike.objects.items().values_list(
        'short_name', flat=True).order_by('date')
    data = models.Data.objects.bike_summary()

    obj = DistanceSummary(years=years, bikes=bikes, data=data)

    # update chart_data with bar color, border color, border_width
    chart_data = obj.chart_data
    for i, dt in enumerate(chart_data):
        dt.update({
            'color': get_color(i, 0.35),
            'borderColor': get_color(i, 1),
            'borderWidth': '0.5',
        })

    context = {
        'year_list': years,
        'chart_data': chart_data[::-1],
        'bikes': bikes,
        'table_data': list(zip(obj.table, obj.total_column)),
        'total_row': obj.total_row,
        'total': sum(obj.total_row.values())
    }
    return render(request, template_name='reports/overall.html', context=context)
