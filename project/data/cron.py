from .library.insert_garmin import SyncWithGarmin
from .library.temperature import Temperature

def cron_insert_from_garmin():

    SyncWithGarmin(Temperature()).insert_data_all_users()
