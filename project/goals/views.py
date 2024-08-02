from django.urls import reverse_lazy

from ..core.mixins.views import (CreateViewMixin, DeleteViewMixin,
                                 ListViewMixin,
                                 UpdateViewMixin)
from ..data.models import Data
from . import forms, models


class GoalList(ListViewMixin):
    template_name = 'goals/goal_list.html'

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
    template_name = 'core/includes/generic_form.html'

    def url(self):
        return reverse_lazy('goals:goal_create')

    def title(self):
        return "New goal"


class GoalUpdate(UpdateViewMixin):
    model = models.Goal
    form_class = forms.GoalForm
    template_name = 'core/includes/generic_form.html'

    def url(self):
        return reverse_lazy('goals:goal_update', kwargs={'pk': self.kwargs['pk']})

    def title(self):
        return "Update goal"


class GoalDelete(DeleteViewMixin):
    model = models.Goal
    template_name = 'core/includes/generic_delete_form.html'
    success_url = '/'

    def url(self):
        return reverse_lazy('goals:goal_delete', kwargs={'pk': self.kwargs['pk']})

    def title(self):
        return "Delete goal"