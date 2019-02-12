from .library.insert_data import insert_data as inserter


def cron_insert_from_endomondo():
    inserter(10)
