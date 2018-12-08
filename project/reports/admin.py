from django.contrib import admin

from . import models


class DataAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Data, DataAdmin)
