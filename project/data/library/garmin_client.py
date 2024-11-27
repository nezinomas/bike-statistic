import garth.http
from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)

from ...core.lib import utils
from . import garmin_exceptions

garth.http.USER_AGENT = {"User-Agent": "GCM-iOS-5.7.2.1",}

class GarminClient:
    def __init__(self, username: str, password: str):
        try:
            self.client = self._client(username, password)
        except Exception as e:
            raise e

    def _client(self, username, password):
        if not username or not password:
            raise garmin_exceptions.NoUsernameOrPassword

        try:
            _client = Garmin(username, utils.decrypt(password))
        except (
            GarminConnectConnectionError,
            GarminConnectAuthenticationError,
            GarminConnectTooManyRequestsError,
        ) as e:
            raise garmin_exceptions.GarminConnectClientInitError(e) from e
        except Exception as e:
            raise garmin_exceptions.GarminConnectClientUknownError(e) from e

        try:
            _client.login()
        except (
            GarminConnectConnectionError,
            GarminConnectAuthenticationError,
            GarminConnectTooManyRequestsError,
        ) as e:
            raise garmin_exceptions.GarminConnectClientLoginError(e) from e
        except Exception as e:
            raise garmin_exceptions.GarminConnectClientUknownError(e) from e

        return _client

    def get_workouts(self, max_results = 10):
        try:
            workouts = self.client.get_activities(0, max_results)
        except (
            GarminConnectConnectionError,
            GarminConnectAuthenticationError,
            GarminConnectTooManyRequestsError,
        ) as e:
            raise garmin_exceptions.GetActivitiesError(e) from e
        except Exception as e:
            raise garmin_exceptions.GetActivitiesUnknownError(e) from e

        return workouts
