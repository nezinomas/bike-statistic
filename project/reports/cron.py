from .library.insert_garmin import insert_data_all_users as inserter


def insert_from_endomondo():
    inserter(10)
