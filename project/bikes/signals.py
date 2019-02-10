import pickle

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Bike, Component

@receiver(post_save, sender=Bike)
@receiver(post_delete, sender=Bike)
def cash_bikes(sender, instance, *args, **kwargs):
    obj = list(Bike.objects.all().values())
    pickle.dump(obj, open("project/bikes/cash/bikes.p", "wb"))


@receiver(post_save, sender=Component)
@receiver(post_delete, sender=Component)
def cash_components(sender, instance, *args, **kwargs):
    obj = list(Component.objects.all().values())
    pickle.dump(obj, open("project/bikes/cash/components.p", "wb"))
