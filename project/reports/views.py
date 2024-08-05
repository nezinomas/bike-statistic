from datetime import datetime

from ..bikes.models import Bike
from ..core.lib import utils
from ..core.mixins.views import TemplateViewMixin
from ..data import models
from .library.chart import get_color
from .library.distance_summary import DistanceSummary
from .library.progress import Progress, ProgressData


class YearProgress(TemplateViewMixin):
    template_name = 'reports/year_progress.html'

    def get_context_data(self, **kwargs):
        year = self.kwargs.get('year') or datetime.now().year
        data = ProgressData(year)
        obj = Progress(data)
        context = {
            'year': year,
            'extremums': obj.extremums(),
            'object_list': obj.season_progress(),
        }
        return super().get_context_data(**kwargs) | context


class ChartOverall(TemplateViewMixin):
    template_name = 'reports/overall.html'

    def get_context_data(self, **kwargs):
        years = utils.years()
        bikes = list(
            Bike.objects.items()
            .values_list('short_name', flat=True).order_by('date'))
        data = list(models.Data.objects.bike_summary())
        obj = DistanceSummary(years, bikes, data)

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
            'chart_overall_data': {'categories': years, 'data': chart_data[::-1]},
            'bikes': bikes,
            'table_data': list(zip(obj.table, obj.total_column)),
            'total_row': obj.total_row,
            'total': sum(obj.total_row.values())
        }

        return super().get_context_data(**kwargs) | context


class Extremums(TemplateViewMixin):
    template_name = 'reports/extremums.html'

    def get_context_data(self, **kwargs):
        obj = Progress(data=ProgressData())
        context = {'object_list': obj.extremums()}
        return super().get_context_data(**kwargs) | context
