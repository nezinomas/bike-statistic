from datetime import date, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views import View

from ..core.lib import utils
from ..core.mixins.views import (
    CreateViewMixin,
    DeleteViewMixin,
    DetailViewMixin,
    ListViewMixin,
    TemplateViewMixin,
    UpdateViewMixin,
    rendered_content,
)
from . import forms, models
from .library.insert_garmin import SyncWithGarmin
from .library.temperature import get_temperature


class DataList(ListViewMixin):
    model = models.Data
    template_name = "data/data_list.html"

    def get_queryset(self):
        now = date.today()
        start_date = self.request.GET.get("start_date") or now - timedelta(20)
        start_date = utils.date_to_datetime(start_date)
        end_date = self.request.GET.get("end_date") or now
        end_date = utils.date_to_datetime(end_date, 23, 59, 59)

        return self.model.objects.items().filter(date__range=(start_date, end_date))

    def get_context_data(self, **kwargs):
        context = {
            "filter_form": forms.DateFilterForm(self.request.GET or None),
        }
        return super().get_context_data(**kwargs) | context


class DataCreate(CreateViewMixin):
    model = models.Data
    form_class = forms.DataForm
    template_name = "core/includes/generic_form.html"
    success_url = reverse_lazy("data:data_list")

    def url(self):
        return reverse_lazy("data:data_create")

    def title(self):
        return "New activity"


class DataUpdate(UpdateViewMixin):
    model = models.Data
    form_class = forms.DataForm
    template_name = "core/includes/generic_form.html"
    success_url = reverse_lazy("data:data_list")

    def url(self):
        return reverse_lazy("data:data_update", kwargs={"pk": self.object.pk})

    def title(self):
        return "Update activity"


class DataUpdateTemperature(DetailViewMixin):
    model = models.Data
    template_name = "data/includes/partial_data_row.html"

    def get_context_data(self, **kwargs):
        temp = get_temperature(self.object.date)
        if temp is not None:
            self.object.temperature = temp
            self.object.save()
        context = {"obj": self.object}
        return super().get_context_data(**kwargs) | context


class QuickUpdate(DetailViewMixin):
    model = models.Data
    template_name = "data/includes/partial_data_row.html"

    def get_context_data(self, **kwargs):
        self.object.checked = "y"
        self.object.save()
        context = {"obj": self.object}
        return super().get_context_data(**kwargs) | context


class DataDelete(DeleteViewMixin):
    model = models.Data
    template_name = "core/includes/generic_delete_form.html"
    success_url = reverse_lazy("data:data_list")

    def url(self):
        return reverse_lazy("data:data_delete", kwargs={"pk": self.object.pk})

    def title(self):
        return "Delete activity"


class DataInsert(TemplateViewMixin):
    template_name = "data/data_insert.html"

    def get(self, *args, **kwargs):
        try:
            SyncWithGarmin().insert_data_current_user()
        except Exception as ex:
            self.kwargs["exception"] = ex
        return super().get(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        if ex := self.kwargs.get("exception"):
            message = (
                f"<p>{ex}</p>"
                f"<p>{'-' * 120}</p>"
                f"<p>Type: {type(ex).__name__}</p>"
                f"<p>Args: {ex.args}</p>"
            )
        else:
            message = rendered_content(self.request, DataList)
        return super().get_context_data(**kwargs) | {"message": message}


class UpdateTodayTemperature(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        get_temperature(now(), force_refresh=True)
        return HttpResponse(rendered_content(request, DataList))
