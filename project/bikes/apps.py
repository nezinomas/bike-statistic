from django.apps import AppConfig


class bikesConfig(AppConfig):
    name = 'project.bikes'

    def ready(self):
        from .signals import cash_bikes
