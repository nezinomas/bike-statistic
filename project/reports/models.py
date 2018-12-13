import datetime

from django.db import models

from ..bikes import models as bikeModels


class Data(models.Model):
    bike = models.ForeignKey(
        bikeModels.Bike,
        on_delete=models.CASCADE,
        related_name='data'
    )
    date = models.DateField(default=datetime.date.today())
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

    def __str__(self):
        return(str(self.date))

    class Meta:
        ordering = ['-date']
