from django.http import JsonResponse
from django.shortcuts import render

from ..library.overall import Overall


def api_overall(request):
    obj = Overall()
    chart = {
        'overall': {
            'xAxis': {'categories': obj.create_categories()},
            'series': obj.create_series()[::-1]
        }
    }
    return JsonResponse(chart)


def overall(request):
    return render(request, template_name='reports/overall.html', context={})
