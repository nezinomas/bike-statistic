from ...bikes.models import Bike
from ...core.lib import utils
from ...users.models import User
from ..models import Data
from . import garmin_exceptions
from .garmin_activity import GarminActivity
from .garmin_client import GarminClient
from .temperature import Temperature


class SyncWithGarmin:
    def __init__(self, temperature: Temperature, client: GarminClient = GarminClient):
        self._client = client
        self._temperature = temperature.temperature

    def insert_data_current_user(self):
        users = [utils.get_user()]
        self._inserter(users)

    def insert_data_all_users(self):
        users = User.objects.all()
        self._inserter(users)

    def _inserter(self, users):
        for user in users:
            try:
                client = self._client(user.garmin_user, user.garmin_password)
            except Exception as e:
                raise e

            try:
                workouts = client.get_workouts()
            except Exception as e:
                raise e

            bike = self._get_bike(user)
            objects = self._prepare_data(user, workouts)
            self._insert_data(user, bike, objects)

    def _prepare_data(self, user, workouts: list[GarminActivity]):
        activities = [GarminActivity(w) for w in workouts]
        last = activities[-1].start_time
        data = list(
            Data.objects.related()
            .filter(date__gte=last)
            .order_by("-date")
            .values_list("date", "distance", "time")
        )

        objects = []
        for activity in activities:
            if not activity.is_valid_activity:
                continue

            tpl = (activity.start_time, activity.distance, activity.duration)
            if tpl in data:
                continue

            objects.append(activity.data_object)
        return objects

    def _insert_data(self, user, bike, objects):
        data = [
            Data(user=user, bike=bike, temperature=self._temperature, **x)
            for x in objects
        ]
        Data.objects.bulk_create(data)

    def _get_bike(self, user):
        bike = Bike.objects.filter(user=user).order_by("pk")

        if not bike.exists():
            raise garmin_exceptions.NoBikeError

        _bike = bike.filter(main=True)
        return _bike[0] if _bike.count() > 0 else bike[0]
