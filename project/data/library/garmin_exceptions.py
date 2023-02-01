class NoUsernameOrPassword(Exception):
    """No Garmin user/password entered"""


class GarminConnectClientInitError(Exception):
    """Error occured during Garmin Connect Client init"""


class GarminConnectClientLoginError(Exception):
    """Error occured during Garmin Connect Client login"""


class GarminConnectClientUknownError(Exception):
    """Unknown error occured during Garmin Connect Client init"""


class GetActivitiesError(Exception):
    """Error occured during Garmin Connect Client get activities"""


class GetActivitiesUnknownError(Exception):
    """Unknown error occured during Garmin Connect Client get activities"""


class NoBikeError(Exception):
    """NAdd at least one Bike"""
