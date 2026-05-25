from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import now

from ...library.temperature import get_temperature


class Command(BaseCommand):
    help = "Fetch and cache today's temperature from Meteo API"

    def handle(self, *args, **options):
        try:
            temp = get_temperature(now(), force_refresh=True)
        except Exception as e:
            raise CommandError(f"Can't fetch temperature - {e}") from e

        self.stdout.write(
            self.style.SUCCESS(
                f"{datetime.now()}: successfully fetched temperature: {temp}"
            )
        )
