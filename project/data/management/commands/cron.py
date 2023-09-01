from datetime import datetime

from django.core.management.base import BaseCommand, CommandError

from ...library.insert_garmin import SyncWithGarmin
from ...library.temperature import Temperature


class Command(BaseCommand):
    help = "Get bike activities from Garmin"

    def handle(self, *args, **options):
        try:
            SyncWithGarmin(Temperature()).insert_data_all_users()
        except Exception as e:
            raise CommandError(f"Can't sync with Garmin - {e}")


        self.stdout.write(
            self.style.SUCCESS(f"{datetime.now()}: successfully get Garmin activities")
        )
