from django.db import models
from django.db.models import Count, F, Sum
from django.db.models.functions import TruncYear

from ..core.lib import utils


class DataQuerySet(models.QuerySet):
    def related(self, user=None):
        user = user or utils.get_user()
        return self.select_related("user", "bike").filter(user=user)

    def _filter_by_year(self, year):
        return self.filter(date__year=year) if year else self

    def items(self, year=None):
        return self.related()._filter_by_year(year)

    def bike_summary(self):
        return (
            self.related()
            .annotate(cnt=Count("bike"))
            .values("bike")
            .annotate(date=TruncYear("date"))
            .values("date")
            .annotate(sum=Sum("distance"))
            .order_by("date")
            .values(
                "date",
                bike=F("bike__short_name"),
                distance=F("sum"),
            )
        )

    def year_distances(self, year=None):
        return (
            self.related()
            ._filter_by_year(year)
            .annotate(year=TruncYear("date"))
            .values("year")
            .annotate(distance=Sum("distance"))
            .order_by("year")
        )
