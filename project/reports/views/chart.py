from ..library.overall import Overall
from .. import models
from django.shortcuts import render
from django.http import JsonResponse


def api_overall(request):
    obj = Overall(models.Data)
    chart = {
        'first': {
            'xAxis': {'categories': obj.create_categories()},
            'series': obj.create_series()[::-1]
        }
    }
    return JsonResponse(chart)


def overall(request):
    return render(request, template_name='reports/overall.html', context={''})
