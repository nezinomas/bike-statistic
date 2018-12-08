from django.db import models
from django.utils.text import slugify


class Goal(models.Model):
    title = models.CharField(
        max_length=254,
        unique=True
    )
    slug = models.SlugField(editable=False)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-end_date']
