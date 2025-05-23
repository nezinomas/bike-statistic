from django.db import models
from django.utils.timezone import now

from ..bikes import models as bike_models
from ..users.models import User
from . import managers


class Data(models.Model):
    # choices
    yes = "y"
    no = "n"
    checked_choices = ((yes, "Yes"), (no, "No"))

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="data")
    bike = models.ForeignKey(
        bike_models.Bike, on_delete=models.CASCADE, related_name="bike_set"
    )
    date = models.DateTimeField(default=now)
    distance = models.FloatField()
    time = models.DurationField()
    temperature = models.FloatField(null=True, blank=True)
    ascent = models.FloatField(default=0.0)
    descent = models.FloatField(default=0.0)
    max_speed = models.FloatField(default=0.0)
    cadence = models.IntegerField(null=True, blank=True)
    heart_rate = models.IntegerField(null=True, blank=True)
    checked = models.CharField(
        max_length=1,
        choices=checked_choices,
        default=no,
    )

    objects = managers.DataQuerySet.as_manager()

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.date:%Y-%m-%d} {self.bike}"
