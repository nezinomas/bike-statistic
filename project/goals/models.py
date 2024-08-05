from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse_lazy

from ..users.models import User
from . import managers


class Goal(models.Model):
    year = models.IntegerField(
        validators=[MinValueValidator(2000), MaxValueValidator(2050)]
    )
    goal = models.IntegerField(
        validators=[MinValueValidator(100), MaxValueValidator(20000)]
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='goals'
    )

    objects = managers.GoalQuerySet.as_manager()

    class Meta:
        ordering = ['-year']
        unique_together = ('user', 'year')

    def __str__(self):
        return str(self.year)

    def get_absolute_url(self):
        return reverse_lazy("goals:goal_list")
