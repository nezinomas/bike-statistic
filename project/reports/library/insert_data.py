from datetime import timedelta

import requests
from lxml import html

from ...bikes.models import Bike
from ...config.secrets import get_secret
from ..endomondo.endomondo import MobileApi
from ..models import Data


def __workouts(maxResults):
    endomondo = MobileApi(email=get_secret("ENDOMONDO_USER"),
                          password=get_secret("ENDOMONDO_PASS"))
    endomondo.get_auth_token()

    return endomondo.get_workouts(maxResults=maxResults)


def get_temperature():
    page = requests.get('https://orai.15min.lt/prognoze/vilnius')
    tree = html.fromstring(page.content)

    tmp = tree.xpath('//div[@class="current-table"]/div[contains(@class, "temperature")]/text()')
    t = ''.join(tmp)

    replace = {'\n': '', '\t': '', '°': ''}

    for key, val in replace.items():
        t = t.replace(key, val)

    return int(t)


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
