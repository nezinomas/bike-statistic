import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ...goals.library.statistic import Statistic


@login_required()
def table(request, year):
    objStats = Statistic(year)
    start = datetime.date(year, 1, 1)
    end = datetime.date(year, 12, 31)

    return render(
        request,
        'reports/table.html',
        {
            'objects': objStats.table(),
            'month': objStats.month_table(),
            'year': year,
            'stats': objStats.stats(start, end)
        }
    )
