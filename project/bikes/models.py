from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.utils.text import slugify


class Bike(models.Model):
    date = models.DateField()
    full_name = models.CharField(
        max_length=150,
        blank=True
    )
    short_name = models.CharField(
        max_length=20,
        unique=True
    )
    slug = models.SlugField(
        editable=False
    )

    def __str__(self):
        return str(self.short_name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.short_name)

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['date']


class BikeInfo(models.Model):
    component = models.CharField(
        max_length=100
    )
    description = models.CharField(
        max_length=254
    )
    bike = models.ForeignKey(
        Bike,
        on_delete=models.CASCADE,
        related_name='bike_info',
    )

    def __str__(self):
        return '{bike}: {component}'.format(self.bike, self.component)


class Component(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        validators=[MaxLengthValidator(99), MinLengthValidator(3)]
    )

    def __str__(self):
        return str(self.name)


class ComponentStatistic(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(
        null=True,
        blank=True
    )
    price = models.FloatField(
        null=True,
        blank=True
    )
    brand = models.TextField(
        blank=True
    )
    bike = models.ForeignKey(
        Bike,
        on_delete=models.CASCADE,
        related_name='bikes'
    )
    component = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        related_name='components'
    )

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return '{bike} / {component} / {start} ... {end}'.format(bike=self.bike, component=self.component, start=self.start_date, end=self.end_date)
