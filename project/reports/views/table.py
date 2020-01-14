from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ...goals.models import Goal
from ..library.progress import Progress


@login_required()
def table(request, year):
    goal = list(
        Goal.objects
        .items()
        .filter(year=year)
        .values_list('goal', flat=True)
    )
    goal = goal[0] if goal else 0

    obj = Progress(year)

    return render(
        request,
        'reports/table.html',
        {
            'year': year,
            'e': obj.extremums().get(year),
            'season': obj.season_progress(goal=goal),
            'month': obj.month_stats(),
        }
    )
