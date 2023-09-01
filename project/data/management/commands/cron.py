from django.core.management.base import BaseCommand

from ...library.insert_garmin import SyncWithGarmin
from ...library.temperature import Temperature


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        SyncWithGarmin(Temperature()).insert_data_all_users()
