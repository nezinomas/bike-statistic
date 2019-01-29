from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator

class Goal(models.Model):
    year = models.IntegerField(
        validators=[MaxLengthValidator(2050), MinLengthValidator(2000)]
    )
    distance = models.IntegerField(
        validators=[MaxLengthValidator(100), MinLengthValidator(20000)]
    )

    def __str__(self):
        return str(self.year)

    class Meta:
        ordering = ['-year']
