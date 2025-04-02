from dataclasses import dataclass, field
from datetime import datetime, timedelta

from django.utils.timezone import make_aware


@dataclass
class GarminActivity:
    data: dict = field(repr=False)
    name: str = field(init=False)
    start_time: datetime = field(init=False)
    distance: float = field(init=False)
    duration: timedelta = field(init=False)
    max_speed: float = field(init=False)
    ascent: int = field(init=False, default=None)
    descent: int = field(init=False, default=None)
    avg_hr: int = field(init=False, default=None)
    avg_cadence: int = field(init=False, default=None)
    is_valid_activity: bool = field(init=False, default=False)

    def __post_init__(self):
        self.name = self._name()
        self.start_time = self._start_time()
        self.distance = self._distance()
        self.duration = self._duration()
        self.max_speed = self._max_speed()
        self.ascent = self.data.get("elevationGain")
        self.descent = self.data.get("elevationLoss")
        self.avg_hr = self.data.get("averageHR")
        self.avg_cadence = self.data.get("averageBikingCadenceInRevPerMinute")
        self.is_valid_activity = self._is_valid_activity()

    @property
    def data_object(self):
        return {
            "date": self.start_time,
            "distance": self.distance,
            "time": self.duration,
            "ascent": self.ascent,
            "descent": self.descent,
            "max_speed": self.max_speed,
            "cadence": self.avg_cadence,
            "heart_rate": self.avg_hr,
        }

    def _name(self):
        name = (self.data.get("activityType") or {}).get("typeKey")
        return name.lower()

    def _start_time(self):
        """return datetime object"""
        date = datetime.now()
        if start_time := self.data.get("startTimeLocal"):
            date = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        return make_aware(date)

    def _duration(self):
        """return: timedelta(seconds)"""
        sec = int(duration) if (duration := self.data.get("duration")) else 0
        return timedelta(seconds=sec)

    def _distance(self):
        """return: km"""
        return round(self.data.get("distance", 0) / 1000, 2)

    def _max_speed(self):
        """return: km/h"""
        if speed := self.data.get("maxSpeed"):
            return round(speed * (3600 / 1000), 2)
        return 0

    def _is_valid_activity(self):
        activities = ("cycling", "biking", "commuting")
        return any(x in self.name for x in activities)
