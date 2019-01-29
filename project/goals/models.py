from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Goal(models.Model):
    year = models.IntegerField(
        unique=True,
        validators=[MinValueValidator(2000), MaxValueValidator(2050)]
    )
    distance = models.IntegerField(
        validators=[MinValueValidator(100), MaxValueValidator(20000)]
    )

    def __str__(self):
        return str(self.year)

    class Meta:
        ordering = ['-year']
