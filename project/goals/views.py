from django.urls import reverse_lazy

from ..core.mixins.views import (CreateViewMixin, DeleteViewMixin,
                                 DetailViewMixin, ListViewMixin,
                                 UpdateViewMixin)
from . import forms, models


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


class GoalUpdate(UpdateViewMixin):
    model = models.Goal
    form_class = forms.GoalForm
    template_name = 'goals/goal_form.html'
    detail_view = GoalDetail

    def url(self):
        return reverse_lazy('goals:goal_update', kwargs={'pk': self.kwargs['pk']})


class GoalDelete(DeleteViewMixin):
    model = models.Goal
    template_name = 'goals/goal_confirm_delete.html'
    success_url = '/'
