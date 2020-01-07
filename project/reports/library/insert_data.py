from datetime import timedelta
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from bs4 import BeautifulSoup

from ...bikes.models import Bike
from ...core.lib import utils
from ..endomondo.endomondo import MobileApi
from ..models import Data


def get_workouts(maxResults):
    user = utils.get_user()
    endomondo = MobileApi(
        email=user.endomondo_user,
        password=user.endomondo_password
    )
    endomondo.get_auth_token()

    return endomondo.get_workouts(maxResults=maxResults)


def get_weather_page(page):
    try:
        html = urlopen(page)
        return html
    except (HTTPError, URLError):
        return


def get_temperature():
    url = 'https://www.gismeteo.lt/weather-vilnius-4230/now/'
    page = get_weather_page(url)
    soup = BeautifulSoup(page, 'html.parser')

    element = soup.find('span', {'class': 'nowvalue__text_l'})

    temperature = element.text
    temperature = temperature.replace(',', '.')
    temperature = temperature.replace('−', '-')

    return float(temperature)


def insert_data(maxResults=20):
    _workouts = get_workouts(maxResults=maxResults)

    bike = Bike.objects.order_by('pk')[0]

    try:
        temperature = get_temperature()
    except:
        temperature = None

    for workout in _workouts:
        if workout.name is not None and 'cycling' in workout.name.lower():

            distance = round(workout.distance, 2)

            row_exists = Data.objects.\
                filter(
                    date=workout.start_time,
                    distance=distance,
                    time=timedelta(seconds=workout.duration)
                )

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
                user=utils.get_user()
            )
