from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from ..core.lib import utils


class User(AbstractUser):
    endomondo_id = models.CharField(max_length=12)
    endomondo_user = models.CharField(
        _('Endomondo user'),
        max_length=32
    )
    endomondo_password = models.CharField(
        _('Endomondo password'),
        max_length=254
    )

    def __str__(self):
        return str(self.username)

    def save(self, *args, **kwargs):
        self.endomondo_password = utils.encrypt(self.endomondo_password)

        super().save(*args, **kwargs)
