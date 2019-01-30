from django.db import models
from django.utils.timezone import now

from ..bikes import models as bikeModels


class Data(models.Model):
    # choices
    yes = 'y'
    no = 'n'
    checked_choices = ((yes, 'Yes'), (no, 'No'))

    bike = models.ForeignKey(
        bikeModels.Bike,
        on_delete=models.CASCADE,
        related_name='bike_set'
    )
    date = models.DateField(default=now)
    distance = models.FloatField()
    time = models.DurationField()
    temperature = models.IntegerField(
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

    def __str__(self):
        return(str(self.date))

    class Meta:
        ordering = ['-date']
