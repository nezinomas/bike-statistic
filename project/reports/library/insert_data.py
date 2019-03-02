from datetime import timedelta

from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup

from ...bikes.models import Bike
from ...config.secrets import get_secret
from ..endomondo.endomondo import MobileApi
from ..models import Data


def __workouts(maxResults):
    endomondo = MobileApi(email=get_secret("ENDOMONDO_USER"),
                          password=get_secret("ENDOMONDO_PASS"))
    endomondo.get_auth_token()

    return endomondo.get_workouts(maxResults=maxResults)


def _get_page_content(page):
    try:
        html = urlopen(page)
        return html
    except (HTTPError, URLError):
        return


def get_temperature():
    url = 'https://www.gismeteo.lt/weather-vilnius-4230/now/'
    page = _get_page_content(url)
    soup = BeautifulSoup(page, 'html.parser')

    element = soup.find('span', {'class': 'nowvalue__text_l'})

    t = element.text
    t = t.replace(',', '.')
    t = t.replace('−', '-')

    return float(t)


def insert_data(maxResults=20):
    workouts = __workouts(maxResults=maxResults)

    bike = Bike.objects.order_by('pk')[0]

    try:
        t = get_temperature()
    except:
        t = None

    for w in workouts:
        if w.name is not None and 'cycling' in w.name.lower():

            distance = round(w.distance, 2)

            row_exists = Data.objects.\
                filter(
                    date=w.start_time,
                    distance=distance,
                    time=timedelta(seconds=w.duration)
                )

            if row_exists:
                continue

            Data.objects.create(
                bike=bike,
                date=w.start_time,
                distance=distance,
                time=timedelta(seconds=w.duration),
                ascent=w.ascent,
                descent=w.descent,
                max_speed=w.speed_max,
                heart_rate=w.heart_rate_avg,
                cadence=w.cadence_avg,
                temperature=t
            )
