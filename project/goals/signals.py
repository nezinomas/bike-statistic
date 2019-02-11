import os
import pickle

from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Goal


@receiver(post_save, sender=Goal)
@receiver(post_delete, sender=Goal)
def cash_goals(sender, instance, *args, **kwargs):
    obj = list(Goal.objects.all().values())
    path = os.path.join(settings.CASH_ROOT, 'goals.p')
    pickle.dump(obj, open(path, "wb"))
