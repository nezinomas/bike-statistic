from .library.insert_garmin import SyncWithGarmin


def cron_insert_from_garmin():
    SyncWithGarmin().insert_data_all_users()
