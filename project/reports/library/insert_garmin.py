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


def _client(username, password):
    if not username or not password:
        raise Exception('No Endomondo user/password entered')

    try:
        client = Garmin(username, utils.decrypt(password))
    except (
        GarminConnectConnectionError,
        GarminConnectAuthenticationError,
        GarminConnectTooManyRequestsError,
    ) as err:
        raise Exception("Error occured during Garmin Connect Client init: %s" % err)
    except Exception:  # pylint: disable=broad-except
        raise Exception("Unknown error occured during Garmin Connect Client init")

    try:
        client.login()
    except (
        GarminConnectConnectionError,
        GarminConnectAuthenticationError,
        GarminConnectTooManyRequestsError,
    ) as err:
        raise Exception("Error occured during Garmin Connect Client login: %s" % err)
    except Exception:  # pylint: disable=broad-except
        raise Exception("Unknown error occured during Garmin Connect Client login")

    return client


def _get_weather_page(page):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
        html = requests.get(page, headers=headers)
        return html.text

    except Exception:
        return


def _insert_data(client, user, temperature, max_results):
    bike = Bike.objects.filter(user=user).order_by('pk')
    if not bike.exists():
        raise Exception('Add at least one Bike.')

    bike = bike[0]  # select first bike

    try:
        workouts = client.get_activities(0, max_results)
    except (
        GarminConnectConnectionError,
        GarminConnectAuthenticationError,
        GarminConnectTooManyRequestsError,
    ) as err:
        raise Exception("Error occured during Garmin Connect Client get activities: %s" % err)

    except Exception:  # pylint: disable=broad-except
        raise Exception("Unknown error occured during Garmin Connect Client get activities")

    for w in workouts:
        workout = GarminActivity(w)

        if workout.name is not None and 'biking' in workout.name.lower():

            row_exists = (
                Data.objects.filter(
                    date=workout.start_time,
                    distance=workout.distance,
                    time=timedelta(seconds=workout.duration),
                    user=user
                ))

            if row_exists:
                continue

            Data.objects.create(
                bike=bike,
                date=workout.start_time,
                distance=workout.distance,
                time=timedelta(seconds=workout.duration),
                ascent=workout.ascent,
                descent=workout.descent,
                max_speed=workout.max_speed,
                heart_rate=workout.avg_hr,
                cadence=workout.avg_candece,
                temperature=temperature,
                user=user
            )


def get_temperature():
    url = 'https://www.gismeteo.lt/weather-vilnius-4230/now/'
    page = _get_weather_page(url)
    soup = BeautifulSoup(page, 'html.parser')

    element = soup.find('span', {'class': 'nowvalue__text_l'})

    temperature = element.text
    temperature = temperature.replace(',', '.')
    temperature = temperature.replace('−', '-')

    return float(temperature)


def insert_data_current_user(max_results=1):
    try:
        temperature = get_temperature()
    except:
        temperature = None

    user = utils.get_user()

    try:
        client = _client(username=user.endomondo_user,
                         password=user.endomondo_password)
    except Exception as e:
        raise Exception(str(e))

    _insert_data(client, user, temperature, max_results)


def insert_data_all_users(max_results=20):
    try:
        temperature = get_temperature()
    except:
        temperature = None

    users = User.objects.all()

    for user in users:
        try:
            client = _client(username=user.endomondo_user,
                             password=user.endomondo_password)
        except:
            continue

        _insert_data(client, user, temperature, max_results)


class GarminActivity():
    def __init__(self, data):
        self.name = (data.get('activityType') or {}).get('typeKey')
        self._start_time = data.get('startTimeLocal')
        self._distance = data.get('distance')
        self._duration = data.get('movingDuration')
        self.ascent = data.get('elevationGain')
        self.descent = data.get('elevationLoss')
        self._max_speed = data.get('maxSpeed')
        self.avg_hr = data.get('averageHR')
        self.avg_candece = data.get('avgStrokeCadence')

    @property
    def start_time(self):
        return datetime.strptime(self._start_time, "%Y-%m-%d %H:%M:%S")

    @property
    def duration(self):
        return int(self._duration)

    @property
    def distance(self):
        return round(self._distance / 1000, 2)

    @property
    def max_speed(self):
        speed = self._max_speed * (3600 / 1000)
        return round(speed, 2)
