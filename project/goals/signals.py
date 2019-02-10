import pickle

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Goal

@receiver(post_save, sender=Goal)
@receiver(post_delete, sender=Goal)
def cash_goals(sender, instance, *args, **kwargs):
    obj = list(Goal.objects.all().values())
    pickle.dump(obj, open("project/goals/cash/goals.p", "wb"))
