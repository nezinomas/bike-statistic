from datetime import datetime, timedelta

from django.test import TestCase

from ..models import Data
from ..factories import BikeFactory, DataFactory
from ..library.overall import Overall


class OverallTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        bike1 = BikeFactory(short_name='bike1', full_name='bike1', date=datetime(1999, 1, 1).date())
        bike2 = BikeFactory(short_name='bike2', full_name='bike2', date=datetime(2000, 1, 1).date())

        DataFactory(bike=bike1, date=datetime(2017, 1, 1).date(), distance=10.0, time=timedelta(seconds=15))
        DataFactory(bike=bike1, date=datetime(2018, 1, 1).date(), distance=100.0, time=timedelta(seconds=15))
        DataFactory(bike=bike2, date=datetime(2017, 1, 1).date(), distance=200.0, time=timedelta(seconds=15))

    def test_create_categories(self):
        obj = Overall(Data)

        expected = [2017, 2018]

        self.assertListEqual(expected, obj.create_categories())

    def test_create_series(self):
        obj = Overall(Data).create_series()

        self.assertEqual(2, len(obj))

        # bike1
        self.assertEqual('bike1', obj[0]['name'], 'bike1 name error')
        self.assertListEqual([10.0, 100.0], obj[0]['data'], 'bike1 data error')

        # bike2
        self.assertEqual('bike2', obj[1]['name'], 'bike2 name error')
        self.assertListEqual([200.0, 0.0], obj[1]['data'], 'bike2 data error')
