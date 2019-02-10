from django.apps import AppConfig


class goalsConfig(AppConfig):
    name = 'project.goals'

    def ready(self):
        from .signals import cash_goals
