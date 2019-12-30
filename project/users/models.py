from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


class User(AbstractUser):
    endomondo_id = models.CharField(max_length=12)
    endomondo_user = models.CharField(
        _('Endomondo user'),
        max_length=32
    )
    endomondo_password = models.CharField(
        _('Endomondo password'),
        max_length=128
    )

    def __str__(self):
        return str(self.username)
