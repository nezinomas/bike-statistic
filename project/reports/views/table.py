import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ...core.lib.stats_goals import StatsGoals


@login_required()
def table(request, year):
    objStats = StatsGoals(year)

    return render(
        request,
        'reports/table.html',
        {
            'objects': objStats.table(),
            'month': objStats.month_stats(),
            'year': year,
            'stats': objStats.year_stats()
        }
    )
