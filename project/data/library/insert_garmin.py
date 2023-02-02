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

            try:
                self._insert_data(user, workouts)
            except Exception as e:
                raise garmin_exceptions.WriteDataToDbError(e) from e

    def _insert_data(self, user, workouts: list[GarminActivity]):
        bike = self._get_bike(user)

        objects = []
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

            objects.append(
                Data(user=user, bike=bike, temperature=self._temperature, **workout.data_object)
            )

        Data.objects.bulk_create(objects)

    def _get_bike(self, user):
        bike = Bike.objects.filter(user=user).order_by('pk')

        if not bike.exists():
            raise garmin_exceptions.NoBikeError

        _bike = bike.filter(main=True)
        return _bike[0] if _bike.count() > 0 else bike[0]
