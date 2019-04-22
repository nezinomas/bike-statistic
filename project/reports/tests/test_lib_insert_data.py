from datetime import datetime, timedelta

import pytest
from mock import patch

from ...core.factories import BikeFactory, DataFactory, UserFactory
from ..endomondo import Workout
from ..library.insert_data import insert_data
