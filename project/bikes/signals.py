import os
import pickle

from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Bike, Component


@receiver(post_save, sender=Bike)
@receiver(post_delete, sender=Bike)
def cash_bikes(sender, instance, *args, **kwargs):
    obj = list(Bike.objects.all().values())
    path = os.path.join(settings.CASH_ROOT, 'bikes.p')
    pickle.dump(obj, open(path, "wb"))


@receiver(post_save, sender=Component)
@receiver(post_delete, sender=Component)
def cash_components(sender, instance, *args, **kwargs):
    obj = list(Component.objects.all().values())
    path = os.path.join(settings.CASH_ROOT, 'components.p')
    pickle.dump(obj, open(path, "wb"))
