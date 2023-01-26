from django.urls import reverse_lazy
from django.shortcuts import reverse, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from ..core.mixins.views import (CreateViewMixin, DeleteViewMixin,
                                 DetailViewMixin, ListViewMixin,
                                 RedirectViewMixin, UpdateViewMixin)
from . import models, forms

from ..reports.library.progress import Progress

def form_valid(data):
    goals = models.Goal.objects.items()

    # obj = Progress()
    # stats = obj.extremums()
    # distances = obj.distances()

    data['form_is_valid'] = True
    # data['html_list'] = render_to_string(
    #     'goals/includes/partial_goals_list.html',
    #     {'goals': goals, 'stats': stats, 'distances': distances}
    # )


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


class GoalDetail(DetailViewMixin):
    model = models.Goal
    template_name = 'goals/includes/partial_goal_row.html'


class GoalList(ListViewMixin):
    def get_template_names(self):
        if self.request.htmx:
            return ['goals/includes/partial_goal_list.html']
        return ['goals/goal_list.html']

    def get_queryset(self):
        return models.Goal.objects.items()


class GoalCreate(CreateViewMixin):
    model = models.Goal
    form_class = forms.GoalForm
    template_name = 'goals/goal_form.html'
    detail_view = GoalDetail

    def url(self):
        return reverse_lazy('goals:goal_create')


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
