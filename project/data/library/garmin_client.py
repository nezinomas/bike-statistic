import contextlib
from pathlib import Path

import requests
from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
    GarthHTTPError,
)

from ...core.lib import utils
from . import garmin_exceptions
from django.conf import settings


class GarminClient:
    def __init__(self, username: str, password: str):
        try:
            self.client = self._client(username, password)
        except Exception as e:
            raise e

    def _client(self, username, password):
        if not username or not password:
            raise garmin_exceptions.NoUsernameOrPasswordError

        tokenstore_path = Path(settings.ENV['GARMIN_TOKEN_STORE']).expanduser()

        # First try to login with stored tokens
        with contextlib.suppress(
            FileNotFoundError,
            GarthHTTPError,
            GarminConnectAuthenticationError,
            GarminConnectConnectionError,
        ):
            garmin = Garmin()
            garmin.login(str(tokenstore_path))
            return garmin

        try:
            garmin = Garmin(email=username, password=utils.decrypt(password), is_cn=False, return_on_mfa=False)
            garmin.login()

            # Save tokens for future use
            garmin.garth.dump(str(tokenstore_path))
            return garmin

        except (
            GarminConnectAuthenticationError,
            FileNotFoundError,
            GarthHTTPError,
            GarminConnectConnectionError,
            requests.exceptions.HTTPError,
        ):
            return None

        except KeyboardInterrupt:
            return None

    def get_workouts(self, max_results=10):
        if not self.client:
            raise Exception("Garmin client is not initialized")

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
