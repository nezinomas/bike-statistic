import datetime

from django.shortcuts import reverse, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse

from .models import Goal
from .forms import GoalForm

from .library.statistic import Statistic


def form_valid(data):
    objects = Statistic().objects()
    data['form_is_valid'] = True
    data['html_list'] = render_to_string(
        'goals/includes/partial_goals_list.html',
        {'objects': objects}
    )


def save_data(request, context, form):
    data = {}

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            form_valid(data)
        else:
            data['form_is_valid'] = False

    context['form'] = form
    data['html_form'] = render_to_string(
        template_name='goals/includes/partial_goals_update.html',
        context=context,
        request=request
    )
    return JsonResponse(data)


@login_required()
def goals_list(request):
    objects = Statistic().objects()
    rendered = render(request, 'goals/goals_list.html', {'objects': objects})
    return rendered


@login_required()
def goals_create(request):
    form = GoalForm(request.POST or None)
    context = {'url': reverse('goals:goals_create')}
    return save_data(request, context, form)


@login_required()
def goals_update(request, year):
    object = get_object_or_404(Goal, year=year)
    form = GoalForm(request.POST or None, instance=object)
    url = reverse('goals:goals_update', kwargs={'year': year})
    context = {'url': url}
    return save_data(request, context, form)


@login_required()
def goals_delete(request, year):
    object = get_object_or_404(Goal, year=year)
    data = {}

    if request.method == 'POST':
        object.delete()
        form_valid(data)
    else:
        context = {'object': object}
        data['html_form'] = render_to_string(
            'goals/includes/partial_goals_delete.html',
            context,
            request
        )
    return JsonResponse(data)


@login_required()
def goals_table(request, year):
    objStats = Statistic(year)
    start = datetime.date(year, 1, 1)
    end = datetime.date(year, 12, 31)

    return render(
        request,
        'goals/goals_table.html',
        {
            'objects': objStats.table(),
            'month': objStats.month_table(),
            'year': year,
            'stats': objStats.stats(start, end)
        }
    )
