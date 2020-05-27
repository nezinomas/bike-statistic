from .library.insert_garmin import SyncWithGarmin


def insert_from_endomondo():
    SyncWithGarmin().insert_data_all_users()
