from dataclasses import dataclass, field
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from django.utils.timezone import make_aware
from garminconnect import (Garmin, GarminConnectAuthenticationError,
                           GarminConnectConnectionError,
                           GarminConnectTooManyRequestsError)

from ...bikes.models import Bike
from ...core.lib import utils
from ...users.models import User
from ..models import Data
from . import garmin_exceptions


class SyncWithGarmin():
    def __init__(self, max_results=10):
        self._max_results = max_results
        self._temperature = Temperature().temperature

    def insert_data_current_user(self):
        users = [utils.get_user()]
        self._inserter(users)

    def insert_data_all_users(self):
        users = User.objects.all()
        self._inserter(users)

    def _inserter(self, users):
        for user in users:
            try:
                client = self._client(
                    username=user.garmin_user,
                    password=user.garmin_password
                )
            except Exception as e:
                raise e

            try:
                self._insert_data(client, user)
            except Exception as e:
                raise garmin_exceptions.WriteDataToDbError from e


    def _client(self, username, password):
        if not username or not password:
            raise garmin_exceptions.NoUsernameOrPassword

        try:
            client = Garmin(username, utils.decrypt(password))
        except (
            GarminConnectConnectionError,
            GarminConnectAuthenticationError,
            GarminConnectTooManyRequestsError,
        ) as e:
            raise garmin_exceptions.GarminConnectClientInitError from e
        except Exception as e:
            raise garmin_exceptions.GarminConnectClientUknownError from e

        try:
            client.login()
        except (
            GarminConnectConnectionError,
            GarminConnectAuthenticationError,
            GarminConnectTooManyRequestsError,
        ) as e:
            raise garmin_exceptions.GarminConnectClientLoginError from e
        except Exception as e:
            raise garmin_exceptions.GarminConnectClientUknownError from e

        return client

    def _insert_data(self, client, user):
        bike = self._get_bike(user)
        workouts = self._get_workouts(client)

        for w in workouts:
            workout = GarminActivity(w)

            if not workout.is_valid_activity:
                continue

            row_exists = (
                Data.objects.filter(
                    date=workout.start_time,
                    distance=workout.distance,
                    time=workout.duration,
                    user=user
                ))

            if row_exists:
                continue

            Data.objects.create(
                bike=bike,
                date=workout.start_time,
                distance=workout.distance,
                time=workout.duration,
                ascent=workout.ascent,
                descent=workout.descent,
                max_speed=workout.max_speed,
                heart_rate=workout.avg_hr,
                cadence=workout.avg_cadence,
                temperature=self._temperature,
                user=user
            )

    def _get_bike(self, user):
        bike = Bike.objects.filter(user=user).order_by('pk')

        if not bike.exists():
            raise garmin_exceptions.NoBikeError

        _bike = bike.filter(main=True)
        return _bike[0] if _bike.count() > 0 else bike[0]

    def _get_workouts(self, client):
        try:
            workouts = client.get_activities(0, self._max_results)
        except (
            GarminConnectConnectionError,
            GarminConnectAuthenticationError,
            GarminConnectTooManyRequestsError,
        ) as e:
            raise garmin_exceptions.GetActivitiesError from e
        except Exception as e:
            raise garmin_exceptions.GetActivitiesUnknownError from e

        return workouts


class Temperature():
    _url = 'https://www.gismeteo.lt/weather-vilnius-4230/now/'

    def __init__(self):
        try:
            self._temperature = self._get_temperature()
        except Exception:  # pylint: disable=broad-except
            self._temperature = None

    @property
    def temperature(self):
        return self._temperature

    def _get_temperature(self):
        page = self._get_weather_page()
        soup = BeautifulSoup(page, 'html.parser')

        element = soup.find('span', {'class': 'unit_temperature_c'})

        temperature = element.text
        temperature = temperature.replace(',', '.')
        temperature = temperature.replace('−', '-')

        return float(temperature)

    def _get_weather_page(self):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
            html = requests.get(self._url, headers=headers)
            return html.text

        except Exception:  # pylint: disable=broad-except
            return ''
