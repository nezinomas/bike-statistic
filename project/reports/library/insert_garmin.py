from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from garminconnect import (Garmin, GarminConnectAuthenticationError,
                           GarminConnectConnectionError,
                           GarminConnectTooManyRequestsError)

from ...bikes.models import Bike
from ...core.lib import utils
from ...users.models import User
from ..models import Data


class SyncWithGarmin():
    activities = ('cycling', 'biking', 'commuting')

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
                    username=user.endomondo_user,
                    password=user.endomondo_password
                )
            except Exception:  # pylint: disable=broad-except
                continue

            self._insert_data(client, user)

    def _client(self, username, password):
        if not username or not password:
            raise Exception('No Endomondo user/password entered')

        try:
            client = Garmin(username, utils.decrypt(password))
        except (
            GarminConnectConnectionError,
            GarminConnectAuthenticationError,
            GarminConnectTooManyRequestsError,
        ) as err:
            raise Exception(
                "Error occured during Garmin Connect Client init: %s" % err)
        except Exception:  # pylint: disable=broad-except
            raise Exception(
                "Unknown error occured during Garmin Connect Client init")

        try:
            client.login()
        except (
            GarminConnectConnectionError,
            GarminConnectAuthenticationError,
            GarminConnectTooManyRequestsError,
        ) as err:
            raise Exception(
                "Error occured during Garmin Connect Client login: %s" % err)
        except Exception:  # pylint: disable=broad-except
            raise Exception(
                "Unknown error occured during Garmin Connect Client login")

        return client

    def _insert_data(self, client, user):
        bike = self._get_bike(user)
        workouts = self._get_workouts(client)

        for w in workouts:
            workout = GarminActivity(w)

            if any(activity in workout.name.lower() for activity in self.activities):
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
            raise Exception('Add at least one Bike.')

        return bike[0]  # select first bike

    def _get_workouts(self, client):
        try:
            workouts = client.get_activities(0, self._max_results)
        except (
            GarminConnectConnectionError,
            GarminConnectAuthenticationError,
            GarminConnectTooManyRequestsError,
        ) as err:
            raise Exception(
                "Error occured during Garmin Connect Client get activities: %s" % err)
        except Exception:  # pylint: disable=broad-except
            raise Exception(
                "Unknown error occured during Garmin Connect Client get activities")

        return workouts

class GarminActivity():
    name = None
    ascent = 0
    descent = 0
    avg_hr = None
    avg_cadence = None

    _start_time = None
    _distance = 0.0
    _duration = 0
    _max_speed = 0

    def __init__(self, data):
        self.name = (data.get('activityType') or {}).get('typeKey')
        self.ascent = data.get('elevationGain')
        self.descent = data.get('elevationLoss')
        self.avg_hr = data.get('averageHR')
        self.avg_cadence = data.get('averageBikingCadenceInRevPerMinute')

        self._start_time = data.get('startTimeLocal')
        self._distance = data.get('distance')  # meters
        self._duration = data.get('duration')  # seconds
        self._max_speed = data.get('maxSpeed')  # meter/second

    @property
    def start_time(self):
        date = datetime.now()

        if self._start_time:
            date = datetime.strptime(self._start_time, "%Y-%m-%d %H:%M:%S")

        return date

    @property
    def duration(self):
        seconds = int(self._duration)
        return timedelta(seconds=seconds)

    @property
    def distance(self):
        return round(self._distance / 1000, 2)

    @property
    def max_speed(self):
        speed = self._max_speed * (3600 / 1000)
        return round(speed, 2)


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

        element = soup.find('span', {'class': 'nowvalue__text_l'})

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
