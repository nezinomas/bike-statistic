from . import models


def bike_list(context):
    q = models.Bike.objects.all()
    return {'bike_list': q}
