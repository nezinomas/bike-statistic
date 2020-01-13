from calendar import monthrange
from datetime import datetime

from django.template.loader import render_to_string
from django.http import JsonResponse

from ..models import Data


def format_date(day=1):
    now = datetime.now()
    year = now.year
    month = now.month
    day = day if day == 1 else monthrange(year, month)[1]

    return '{y}-{m:02d}-{d:02d}'.format(y=year, m=month, d=day)


def form_valid(data, start_date, end_date):
    data['form_is_valid'] = True
    objects = (
        Data.objects
        .items()
        .filter(date__range=(start_date, end_date))
    )
    data['html_list'] = render_to_string(
        'reports/includes/partial_data_list.html',
        {
            'objects': objects,
            'start_date': start_date,
            'end_date': end_date,
        }
    )


def save_data(request, context, form, start_date, end_date):
    data = {}

    if request.method == 'POST':
        if form.is_valid():

            f = form.save(commit=False)
            f.checked = 'y'
            f.save()

            form_valid(data, start_date, end_date)
        else:
            data['form_is_valid'] = False

    context['form'] = form
    data['html_form'] = render_to_string(
        'reports/includes/partial_data_update.html', context, request)

    return JsonResponse(data)
