from django.db import models
from django.db.models import Count, F, Sum
from django.db.models.functions import TruncYear
from django.utils.timezone import now

from ..bikes import models as bikeModels
from ..core.lib import utils
from ..users.models import User


class DataQuerySet(models.QuerySet):
    def related(self):
        user = utils.get_user()
        return (
            self
            .select_related('user', 'bike')
            .filter(user=user)
        )

    def _filter_by_year(self, year):
        return self.filter(date__year=year) if year else self

    def items(self, year=None):
        return self.related()._filter_by_year(year)

    def bike_summary(self):
        return (
            self
            .related()
            .annotate(cnt=Count('bike'))
            .values('bike')
            .annotate(date=TruncYear('date'))
            .values('date')
            .annotate(sum=Sum('distance'))
            .order_by('date')
            .values(
                'date',
                bike=F('bike__short_name'),
                distance=F('sum'),
            )
        )


class Data(models.Model):
    # choices
    yes = 'y'
    no = 'n'
    checked_choices = ((yes, 'Yes'), (no, 'No'))

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='data'
    )
    bike = models.ForeignKey(
        bikeModels.Bike,
        on_delete=models.CASCADE,
        related_name='bike_set'
    )
    date = models.DateField(default=now)
    distance = models.FloatField()
    time = models.DurationField()
    temperature = models.FloatField(
        null=True,
        blank=True
    )
    ascent = models.FloatField(
        default=0.0
    )
    descent = models.FloatField(
        default=0.0
    )
    max_speed = models.FloatField(
        default=0.0
    )
    cadence = models.IntegerField(
        null=True,
        blank=True
    )
    heart_rate = models.IntegerField(
        null=True,
        blank=True
    )
    checked = models.CharField(
        max_length=1,
        choices=checked_choices,
        default=no,
    )

    objects = DataQuerySet.as_manager()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.date:%Y-%m-%d} {self.bike}'
