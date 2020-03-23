from datetime import timedelta

import requests
from bs4 import BeautifulSoup

from ...bikes.models import Bike
from ...core.lib import utils
from ...users.models import User
from ..endomondo.endomondo import MobileApi
from ..models import Data


def _endomondo_api(endomondo_user, endomondo_password):
    if not endomondo_user or not endomondo_password:
        raise Exception('No Endomondo user/password entered')

    api = MobileApi(
        email=endomondo_user,
        password=utils.decrypt(endomondo_password)
    )
    api.get_auth_token()

    return api


def _get_workouts(api, max_results):
    return api.get_workouts(maxResults=max_results)


def _get_weather_page(page):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
        html = requests.get(page, headers=headers)
        return html.text

    except Exception:
        return


def _insert_data(api, user, temperature, max_results):
    bike = Bike.objects.filter(user=user).order_by('pk')
    if not bike.exists():
        raise Exception('Add at least one Bike.')

    bike = bike[0] # select first bike

    workouts = _get_workouts(api=api, max_results=max_results)

    for workout in workouts:
        if workout.name is not None and 'cycling' in workout.name.lower():

            distance = round(workout.distance, 2)

            row_exists = (
                Data.objects.filter(
                    date=workout.start_time,
                    distance=distance,
                    time=timedelta(seconds=workout.duration),
                    user=user
                ))

            if row_exists:
                continue

            Data.objects.create(
                bike=bike,
                date=workout.start_time,
                distance=distance,
                time=timedelta(seconds=workout.duration),
                ascent=workout.ascent,
                descent=workout.descent,
                max_speed=workout.speed_max,
                heart_rate=workout.heart_rate_avg,
                cadence=workout.cadence_avg,
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


def insert_data_current_user(max_results=20):
    try:
        temperature = get_temperature()
    except:
        temperature = None

    user = utils.get_user()

    try:
        api = _endomondo_api(endomondo_user=user.endomondo_user,
                             endomondo_password=user.endomondo_password)
    except Exception as e:
        raise Exception(str(e))

    _insert_data(api, user, temperature, max_results)


def insert_data_all_users(max_results=20):
    try:
        temperature = get_temperature()
    except:
        temperature = None

    users = User.objects.all()

    for user in users:
        try:
            api = _endomondo_api(endomondo_user=user.endomondo_user,
                                endomondo_password=user.endomondo_password)
        except:
            continue

        _insert_data(api, user, temperature, max_results)
