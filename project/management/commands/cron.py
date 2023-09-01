from django.core.management.base import BaseCommand

from ...data.library.insert_garmin import SyncWithGarmin
from ...data.library.temperature import Temperature


class Cron(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        SyncWithGarmin(Temperature()).insert_data_all_users()
