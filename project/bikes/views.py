from django.urls import reverse_lazy

from ..core.mixins.views import (CreateViewMixin, DeleteViewMixin,
                                 ListViewMixin,
                                 UpdateViewMixin)
from ..data.models import Data
from . import forms, models
from .lib.component_wear import ComponentWear


class BikeList(ListViewMixin):
    template_name = "bikes/bike_list.html"

    def get_queryset(self):
        return models.Bike.objects.items()


class BikeCreate(CreateViewMixin):
    model = models.Bike
    form_class = forms.BikeForm
    template_name = "core/includes/generic_form.html"

    def url(self):
        return reverse_lazy("bikes:bike_create")

    def title(self):
        return "Create Bike"


class BikeUpdate(UpdateViewMixin):
    model = models.Bike
    form_class = forms.BikeForm
    template_name = "core/includes/generic_form.html"

    def url(self):
        return reverse_lazy("bikes:bike_update", kwargs={"pk": self.kwargs["pk"]})

    def title(self):
        return "Update Bike"


class BikeDelete(DeleteViewMixin):
    model = models.Bike
    template_name = "core/includes/generic_delete_form.html"
    success_url = "/"

    def url(self):
        return reverse_lazy("bikes:bike_delete", kwargs={"pk": self.kwargs["pk"]})

    def title(self):
        return "Delete Bike"

    def message(self):
        return "Warning: all activities related to this bike will be deleted!"


# ---------------------------------------------------------------------------------------
#                                                                               Bike Info
# ---------------------------------------------------------------------------------------
class BikeInfoList(ListViewMixin):
    template_name = "bikes/info_list.html"

    def get_queryset(self):
        return models.BikeInfo.objects.items().filter(
            bike__slug=self.kwargs["bike_slug"]
        )


class BikeInfoCreate(CreateViewMixin):
    model = models.BikeInfo
    template_name = "core/includes/generic_form.html"

    def url(self):
        return reverse_lazy(
            "bikes:info_create", kwargs={"bike_slug": self.kwargs["bike_slug"]}
        )

    def get_form(self, data=None, files=None, **kwargs):
        # pass bike_slug and component_pk from self.kwargs to form
        return forms.BikeInfoForm(data, files, **kwargs | self.kwargs)

    def title(self):
        return "New Bike Info"


class BikeInfoUpdate(UpdateViewMixin):
    model = models.BikeInfo
    form_class = forms.BikeInfoForm
    template_name = "core/includes/generic_form.html"

    def url(self):
        return reverse_lazy(
            "bikes:info_update",
            kwargs={"bike_slug": self.kwargs["bike_slug"], "pk": self.kwargs["pk"]},
        )

    def title(self):
        return "Update Bike Info"


class BikeInfoDelete(DeleteViewMixin):
    model = models.BikeInfo
    template_name = "core/includes/generic_delete_form.html"
    success_url = "/"

    def url(self):
        return reverse_lazy(
            "bikes:info_delete",
            kwargs={"bike_slug": self.kwargs["bike_slug"], "pk": self.kwargs["pk"]},
        )

    def title(self):
        return "Delete Bike Info"


# ---------------------------------------------------------------------------------------
#                                                                              Components
# ---------------------------------------------------------------------------------------
class ComponentList(ListViewMixin):
    template_name = "bikes/component_list.html"

    def get_queryset(self):
        return models.Component.objects.items()


class ComponentCreate(CreateViewMixin):
    model = models.Component
    form_class = forms.ComponentForm
    template_name = "core/includes/generic_form.html"

    def url(self):
        return reverse_lazy("bikes:component_create")

    def title(self):
        return "New Component"


class ComponentUpdate(UpdateViewMixin):
    model = models.Component
    form_class = forms.ComponentForm
    template_name = "core/includes/generic_form.html"

    def url(self):
        return reverse_lazy("bikes:component_update", kwargs={"pk": self.kwargs["pk"]})

    def title(self):
        return "Update Component"


class ComponentDelete(DeleteViewMixin):
    model = models.Component
    template_name = "core/includes/generic_delete_form.html"
    success_url = "/"

    def url(self):
        return reverse_lazy("bikes:component_delete", kwargs={"pk": self.kwargs["pk"]})

    def title(self):
        return "Delete Component"


# ---------------------------------------------------------------------------------------
#                                                                     Bike Component Wear
# ---------------------------------------------------------------------------------------
class ComponentWearList(ListViewMixin):
    template_name = "bikes/component_wear_list.html"

    def get_queryset(self):
        return models.Component.objects.items()

    def get_context_data(self, **kwargs):
        bike = models.Bike.objects.related().get(slug=self.kwargs["bike_slug"])
        component_pk = self.kwargs.get("component_pk")
        if not component_pk:
            component = models.Component.objects.related().first()
        else:
            component = models.Component.objects.related().get(pk=component_pk)

        data = Data.objects.items().filter(bike=bike).values("date", "distance")

        component_statistic = models.ComponentWear.objects.items().filter(
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


class ComponentWearCreate(CreateViewMixin):
    model = models.ComponentWear
    template_name = "core/includes/generic_form.html"

    def url(self):
        return reverse_lazy(
            "bikes:wear_create",
            kwargs={
                "bike_slug": self.kwargs["bike_slug"],
                "component_pk": self.kwargs["component_pk"],
            },
        )

    def get_form(self, data=None, files=None, **kwargs):
        # pass bike_slug and component_pk from self.kwargs to form
        return forms.ComponentWearForm(data, files, **kwargs | self.kwargs)

    def title(self):
        return "New Component"


class ComponentWearUpdate(UpdateViewMixin):
    model = models.ComponentWear
    form_class = forms.ComponentWearForm
    template_name = "core/includes/generic_form.html"
    lookup_url_kwarg = "wear_pk"

    def url(self):
        return reverse_lazy(
            "bikes:wear_update",
            kwargs={
                "bike_slug": self.kwargs["bike_slug"],
                "wear_pk": self.kwargs["wear_pk"],
            },
        )

    def title(self):
        return "Update Component"


class ComponentWearDelete(DeleteViewMixin):
    model = models.ComponentWear
    template_name = "core/includes/generic_delete_form.html"
    lookup_url_kwarg = "wear_pk"
    success_url = "/"

    def url(self):
        return reverse_lazy(
            "bikes:wear_delete",
            kwargs={
                "bike_slug": self.kwargs["bike_slug"],
                "wear_pk": self.kwargs["wear_pk"],
            },
        )

    def title(self):
        return "Delete Component"