from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from ..core.lib import utils
from ..users.models import User


class GoalQuerySet(models.QuerySet):
    def related(self):
        user = utils.get_user()
        return (
            self
            .select_related('user')
            .filter(user=user)
        )

    def items(self):
        return self.related()


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

    objects = GoalQuerySet.as_manager()

    class Meta:
        ordering = ['-year']
        unique_together = ('user', 'year')

    def __str__(self):
        return str(self.year)
