import contextlib
from datetime import date

from django.db.models import Sum
from django.urls import reverse_lazy

from ..core.lib import utils
from ..core.mixins.views import (
    CreateViewMixin,
    DeleteViewMixin,
    DetailViewMixin,
    ListViewMixin,
    UpdateViewMixin,
)
from ..data.models import Data
from . import forms, models
from .lib.component_wear import ComponentWear


class BikeDetail(DetailViewMixin):
    model = models.Bike
    template_name = "bikes/includes/partial_bike_row.html"


class BikeList(ListViewMixin):
    template_name = "bikes/bike_list.html"

    def get_queryset(self):
        return models.Bike.objects.items()


class BikeMenuList(ListViewMixin):
    template_name = "bikes/bike_menu.html"

    def get_queryset(self):
        return models.Bike.objects.items()

    def get_context_data(self, **kwargs):
        with contextlib.suppress(models.Component.DoesNotExist):
            obj = models.Component.objects.related().first()

        context = {"component": obj or None}
        return super().get_context_data(**kwargs) | context


class BikeCreate(CreateViewMixin):
    model = models.Bike
    form_class = forms.BikeForm
    template_name = "bikes/bike_form.html"
    detail_view = BikeDetail
    hx_trigger_django = "bike_update"

    def url(self):
        return reverse_lazy("bikes:bike_create")


class BikeUpdate(UpdateViewMixin):
    model = models.Bike
    form_class = forms.BikeForm
    template_name = "bikes/bike_form.html"
    detail_view = BikeDetail
    hx_trigger_django = "bike_update"

    def url(self):
        return reverse_lazy("bikes:bike_update", kwargs={"pk": self.kwargs["pk"]})


class BikeDelete(DeleteViewMixin):
    model = models.Bike
    template_name = "bikes/bike_confirm_delete.html"
    success_url = "/"
    hx_trigger_django = "bike_update"


# ---------------------------------------------------------------------------------------
#                                                                               Bike Info
# ---------------------------------------------------------------------------------------
class BikeInfoList(ListViewMixin):
    template_name = "bikes/info_list.html"

    def get_queryset(self):
        return models.BikeInfo.objects.items().filter(
            bike__slug=self.kwargs["bike_slug"]
        )

    def get_context_data(self, **kwargs):
        context = {"bike_list": models.Bike.objects.items()}
        return super().get_context_data(**kwargs) | context


class BikeInfoDetail(DetailViewMixin):
    model = models.BikeInfo
    template_name = "bikes/includes/partial_info_row.html"


class BikeInfoDefaultBike(ListViewMixin):
    template_name = "bikes/bike_info_default_bike.html"

    def get_queryset(self):
        return (
            models.Bike.objects.related().filter(main=True)[:1]
            or models.Bike.objects.related().items()[:1]
        )


class BikeInfoCreate(CreateViewMixin):
    model = models.BikeInfo
    template_name = "bikes/info_form.html"
    detail_view = BikeInfoDetail

    def url(self):
        return reverse_lazy(
            "bikes:info_create", kwargs={"bike_slug": self.kwargs["bike_slug"]}
        )

    def get_form(self, data=None, files=None, **kwargs):
        # pass bike_slug and component_pk from self.kwargs to form
        return forms.BikeInfoForm(data, files, **kwargs | self.kwargs)


class BikeInfoUpdate(UpdateViewMixin):
    model = models.BikeInfo
    form_class = forms.BikeInfoForm
    template_name = "bikes/info_form.html"
    detail_view = BikeInfoDetail

    def url(self):
        return reverse_lazy(
            "bikes:info_update",
            kwargs={"bike_slug": self.kwargs["bike_slug"], "pk": self.kwargs["pk"]},
        )


class BikeInfoDelete(DeleteViewMixin):
    model = models.BikeInfo
    template_name = "bikes/info_confirm_delete.html"
    success_url = "/"


# ---------------------------------------------------------------------------------------
#                                                                              Components
# ---------------------------------------------------------------------------------------
class ComponentDetail(DetailViewMixin):
    model = models.Component
    template_name = "bikes/includes/partial_component_row.html"


class ComponentList(ListViewMixin):
    template_name = "bikes/component_list.html"

    def get_queryset(self):
        return models.Component.objects.items()


class ComponentCreate(CreateViewMixin):
    model = models.Component
    form_class = forms.ComponentForm
    template_name = "bikes/component_form.html"
    detail_view = ComponentDetail

    def url(self):
        return reverse_lazy("bikes:component_create")


class ComponentUpdate(UpdateViewMixin):
    model = models.Component
    form_class = forms.ComponentForm
    template_name = "bikes/component_form.html"
    detail_view = ComponentDetail

    def url(self):
        return reverse_lazy("bikes:component_update", kwargs={"pk": self.kwargs["pk"]})


class ComponentDelete(DeleteViewMixin):
    model = models.Component
    template_name = "bikes/component_confirm_delete.html"
    success_url = "/"


# ---------------------------------------------------------------------------------------
#                                                         Bike Component Statistic (Wear)
# ---------------------------------------------------------------------------------------
class StatsDetail(DetailViewMixin):
    model = models.ComponentStatistic
    lookup_url_kwarg = "stats_pk"
    template_name = "bikes/includes/partial_stats_row.html"

    def get_context_data(self, **kwargs):
        bike_slug = self.kwargs["bike_slug"]
        stats_pk = self.kwargs["stats_pk"]
        start_date = utils.date_to_datetime(self.object.start_date)
        end_date = utils.date_to_datetime(
            self.object.end_date or date.today(), 23, 59, 59
        )

        distance_sum = Data.objects.filter(
            bike__slug=bike_slug, date__range=(start_date, end_date)
        ).aggregate(Sum("distance"))

        context = {
            "km": {str(stats_pk): distance_sum.get("distance__sum", 0)},
        }

        return super().get_context_data(**kwargs) | context


class StatsList(ListViewMixin):
    template_name = "bikes/stats_list.html"

    def get_queryset(self):
        return models.Component.objects.items()

    def get_context_data(self, **kwargs):
        bike = models.Bike.objects.related().get(slug=self.kwargs["bike_slug"])
        component = models.Component.objects.related().get(
            pk=self.kwargs["component_pk"]
        )
        data = Data.objects.items().filter(bike=bike).values("date", "distance")

        component_statistic = models.ComponentStatistic.objects.items().filter(
            bike=bike, component=component
        )

        obj = ComponentWear(
            [*component_statistic.values("start_date", "end_date", "pk")], [*data]
        )
        context = {
            "bike": bike,
            "component": component,
            "component_statistic": component_statistic,
            "km": obj.component_km,
            "stats": obj.component_stats,
            "total": obj.bike_km,
        }
        return super().get_context_data(**kwargs) | context


class StatsCreate(CreateViewMixin):
    model = models.ComponentStatistic
    template_name = "bikes/stats_form.html"
    hx_trigger_django = "reload"

    def url(self):
        return reverse_lazy(
            "bikes:stats_create",
            kwargs={
                "bike_slug": self.kwargs["bike_slug"],
                "component_pk": self.kwargs["component_pk"],
            },
        )

    def get_form(self, data=None, files=None, **kwargs):
        # pass bike_slug and component_pk from self.kwargs to form
        return forms.ComponentStatisticForm(data, files, **kwargs | self.kwargs)


class StatsUpdate(UpdateViewMixin):
    model = models.ComponentStatistic
    form_class = forms.ComponentStatisticForm
    template_name = "bikes/stats_form.html"
    lookup_url_kwarg = "stats_pk"
    hx_trigger_django = "reload"

    def url(self):
        return reverse_lazy(
            "bikes:stats_update",
            kwargs={
                "bike_slug": self.kwargs["bike_slug"],
                "stats_pk": self.kwargs["stats_pk"],
            },
        )


class StatsDelete(DeleteViewMixin):
    model = models.ComponentStatistic
    template_name = "bikes/stats_confirm_delete.html"
    lookup_url_kwarg = "stats_pk"
    success_url = "/"
    hx_trigger_django = "reload"
