from django.urls import reverse_lazy

from ..core.mixins.views import (CreateViewMixin, DeleteViewMixin,
                                 DetailViewMixin, ListViewMixin,
                                 UpdateViewMixin)
from ..data.models import Data
from . import forms, models


class GoalDetail(DetailViewMixin):
    model = models.Goal
    template_name = 'goals/includes/partial_goal_row.html'

    def get_context_data(self, **kwargs):
        year = self.object.year
        qs = Data.objects.year_distances(year)
        context = {
            'distances': {str(year): qs[0]['distance']}
        }
        return super().get_context_data(**kwargs) | context


class GoalList(ListViewMixin):
    def get_template_names(self):
        if self.request.htmx:
            return ['goals/includes/partial_goal_list.html']
        return ['goals/goal_list.html']

    def get_queryset(self):
        return models.Goal.objects.items()

    def get_context_data(self, **kwargs):
        qs = Data.objects.year_distances()
        context = {
            'distances': {str(row['year'].year): row['distance'] for row in qs}
        }
        return super().get_context_data(**kwargs) | context


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
