from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy

from ..core.mixins.views import (CreateViewMixin, DeleteViewMixin,
                                 DetailViewMixin, ListViewMixin, UpdateViewMixin)
from . import forms, models
from .helpers import view_data_helper as helper
from .library.insert_garmin import SyncWithGarmin


class DataDetail(DetailViewMixin):
    model = models.Data
    template_name = 'data/includes/partial_data_row.html'


class DataList(ListViewMixin):
    model = models.Data

    def get_queryset(self):
        start_date = self.request.GET.get('start_date') or helper.format_date(day=1)
        end_date = self.request.GET.get('end_date') or helper.format_date()
        return self.model.objects.items().filter(date__range=(start_date, end_date))

    def get_template_names(self):
        if self.request.htmx:
            return ['data/includes/partial_data_list.html']
        return ['data/data_list.html']

    def get_context_data(self, **kwargs):
        context = {
            'filter_form': forms.DateFilterForm(self.request.GET or None),
        }
        return super().get_context_data(**kwargs) | context


class DataCreate(CreateViewMixin):
    model = models.Data
    form_class = forms.DataForm
    success_url = reverse_lazy('index')
    hx_trigger_django = 'reload'

    def url(self):
        return reverse_lazy('data:data_create')


class DataUpdate(UpdateViewMixin):
    model = models.Data
    form_class = forms.DataForm
    success_url = reverse_lazy('index')
    detail_template_name = 'data/includes/partial_data_row.html'

    def url(self):
        return reverse_lazy('data:data_update', kwargs={'pk': self.object.pk})


class QuickUpdate(DetailViewMixin):
    model = models.Data
    template_name = 'data/includes/partial_data_row.html'

    def get_context_data(self, **kwargs):
        self.object.checked = 'y'
        self.object.save()
        context = {'obj': self.object}
        return super().get_context_data(**kwargs) | context


class DataDelete(DeleteViewMixin):
    model = models.Data
    success_url = reverse_lazy('index')


@login_required()
def insert_data(request):
    try:
        SyncWithGarmin().insert_data_current_user()
    except Exception as ex:
        msg = (
            f'<p>{ex}</p>'
            f'<p>{"-"*120}</p>'
            f'<p>Type: {type(ex).__name__}</p>'
            f'<p>Args: {ex.args}</p>'
        )
        return render(
            request,
            template_name='data/data_insert.html',
            context={'message': msg}
        )
    return redirect(reverse('index'))
