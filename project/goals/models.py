from django.db import models
from django.utils.text import slugify
from django.core.validators import MaxLengthValidator, MinLengthValidator

class Goal(models.Model):
    title = models.CharField(
        max_length=254,
        unique=True
    )
    slug = models.SlugField(editable=False)
    year = models.IntegerField(
        validators=[MaxLengthValidator(2050), MinLengthValidator(2000)]
    )
    distance = models.IntegerField(
        validators=[MaxLengthValidator(100), MinLengthValidator(20000)]
    )

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-year']
