from django.contrib import admin

from . import models


class BikeAdmin(admin.ModelAdmin):
    pass


class BikeNoteAdmin(admin.ModelAdmin):
    pass


class ComponentAdmin(admin.ModelAdmin):
    pass


class ComponentStatisticAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Bike, BikeAdmin)
# admin.site.register(models.BikeInfo, BikeNoteAdmin)
admin.site.register(models.Component, ComponentAdmin)
admin.site.register(models.ComponentStatistic, ComponentStatisticAdmin)
