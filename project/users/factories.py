from datetime import datetime

import factory
import pytz
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save

from ..users.models import User


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    username = "bob"
    password = make_password("123")
    email = "bob@bob.com"
    date_joined = datetime(2000, 1, 1, tzinfo=pytz.UTC)
    garmin_user = "ebob"
    garmin_password = "123"
