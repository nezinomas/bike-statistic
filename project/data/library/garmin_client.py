from garminconnect import (Garmin, GarminConnectAuthenticationError,
                           GarminConnectConnectionError,
                           GarminConnectTooManyRequestsError)

from ...core.lib import utils
from . import garmin_exceptions


class GarminClient:
    def __init__(self, username: str, password: str, client: Garmin):
        try:
            self.client = self._client(username, password, client)
        except Exception as e:
            raise e

    def _client(self, username, password, client: Garmin):
        if not username or not password:
            raise garmin_exceptions.NoUsernameOrPassword

        try:
            _client = client(username, utils.decrypt(password))
        except (
            GarminConnectConnectionError,
            GarminConnectAuthenticationError,
            GarminConnectTooManyRequestsError,
        ) as e:
            raise garmin_exceptions.GarminConnectClientInitError from e
        except Exception as e:
            raise garmin_exceptions.GarminConnectClientUknownError from e

        try:
            _client.login()
        except (
            GarminConnectConnectionError,
            GarminConnectAuthenticationError,
            GarminConnectTooManyRequestsError,
        ) as e:
            raise garmin_exceptions.GarminConnectClientLoginError from e
        except Exception as e:
            raise garmin_exceptions.GarminConnectClientUknownError from e

        return _client

    def get_workouts(self, max_results = 10):
        try:
            workouts = self.client.get_activities(0, max_results)
        except (
            GarminConnectConnectionError,
            GarminConnectAuthenticationError,
            GarminConnectTooManyRequestsError,
        ) as e:
            raise garmin_exceptions.GetActivitiesError from e
        except Exception as e:
            raise garmin_exceptions.GetActivitiesUnknownError from e

        return workouts
