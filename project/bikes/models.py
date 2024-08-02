from django.urls import reverse_lazy
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.utils.text import slugify

from ..core.lib import utils
from ..users.models import User


class BikeQuerySet(models.QuerySet):
    def related(self):
        user = utils.get_user()

        if not user or not user.id:
            return self

        return (
            self
            .select_related('user')
            .filter(user=user)
        )

    def items(self):
        return self.related()


class Bike(models.Model):
    date = models.DateField()
    full_name = models.CharField(
        max_length=150,
        blank=True
    )
    short_name = models.CharField(
        max_length=20,
    )
    slug = models.SlugField(
        editable=False
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bikes'
    )
    main = models.BooleanField(default=False)
    retired = models.BooleanField(default=False)

    objects = BikeQuerySet.as_manager()

    class Meta:
        ordering = ['date']
        unique_together = ('user', 'short_name')

    def __str__(self):
        return str(self.short_name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.short_name)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy("bikes:bike_detail", kwargs={"pk": self.pk})


class BikeInfoQuerySet(models.QuerySet):
    def related(self):
        user = utils.get_user()
        return (
            self
            .select_related('bike')
            .filter(bike__user=user)
        )

    def items(self):
        return self.related()


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

    objects = BikeInfoQuerySet.as_manager()

    class Meta:
        ordering = ['component']

    def __str__(self):
        return f'{self.bike}: {self.component}'

    def get_absolute_url(self):
        return reverse_lazy("bikes:info_list", kwargs={"bike_slug": self.bike.slug})


class ComponentQuerySet(models.QuerySet):
    def related(self):
        user = utils.get_user()
        return (
            self
            .select_related('user')
            .filter(user=user)
        )

    def items(self):
        return self.related()


class Component(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[MaxLengthValidator(99), MinLengthValidator(3)]
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='components'
    )

    objects = ComponentQuerySet.as_manager()

    class Meta:
        ordering = ['name']
        unique_together = ('user', 'name')

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse_lazy("bikes:component_list")


class ComponentStatisticQuerySet(models.QuerySet):
    def related(self):
        user = utils.get_user()
        return (
            self
            .select_related('bike', 'component')
            .filter(bike__user=user)
        )

    def items(self):
        return self.related()


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
    brand = models.CharField(
        blank=True,
        max_length=254
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

    objects = ComponentStatisticQuerySet.as_manager()

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f'{self.bike} / {self.component} / {self.start_date} ... {self.end_date}'

    def get_absolute_url(self):
        return reverse_lazy(
            "bikes:stats_list",
            kwargs={"bike_slug": self.bike.slug, "component_pk": self.pk})
