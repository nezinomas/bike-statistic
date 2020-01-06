from datetime import datetime
from typing import List

from django.shortcuts import render

from ...bikes.models import Bike
from ...core.lib import utils
from ..library.chart import get_color
from ..library.distance_summary import DistanceSummary
from ..models import Data


def _years() -> List[int]:
    now = datetime.now().year
    start = now

    try:
        start = utils.get_user().date_joined.year
    except AttributeError:
        pass

    _years = [x for x in range(start, now)]

    return _years


def overall(request):
    years = _years()
    bikes = Bike.objects.items().values_list('short_name', flat=True).order_by('date')
    data = Data.objects.bike_summary()

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
        'years': years,
        'chart_data': chart_data[::-1],
        'bikes': bikes,
        'body': zip(obj.table, obj.total_column),
        'total_row': obj.total_row,
        'total': sum(obj.total_row.values())
    }
    return render(request, template_name='reports/overall.html', context=context)
