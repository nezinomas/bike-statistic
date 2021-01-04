from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from ..core.lib import utils


class User(AbstractUser):
    garmin_user = models.CharField(
        _('Garmin user'),
        max_length=32
    )
    garmin_password = models.CharField(
        _('Garmin password'),
        max_length=254
    )

    def __str__(self):
        return str(self.username)

    def save(self, *args, **kwargs):
        if self.garmin_user:
            self.garmin_password = utils.encrypt(self.garmin_password)

        super().save(*args, **kwargs)
