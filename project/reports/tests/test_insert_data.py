from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import resolve, reverse
from mock import patch

from .. import models, views
from ..endomondo import Workout
from ..factories import BikeFactory, DataFactory
from ..library.insert_data import insert_data


class GetDataViewTests(TestCase):
    def test_view_status_code_200(self):
        url = reverse('reports:insert_data')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_func(self):
        view = resolve('/data/insert')
        self.assertEqual(view.func, views.insert_data)


class GetDataMethodTests(TestCase):
    def setUp(self):
        patcher_post = patch('project.reports.library.insert_data.__workouts')
        self.mock_call = patcher_post.start()
        self.mock_call.return_value = [Workout(
            {
                'ascent': 9,
                'descent': 9,
                'distance': 10.12345,
                'duration': 15,
                'sport': 2,
                'start_time': '2000-01-01 14:48:05 UTC'
            })]
        self.addCleanup(patcher_post.stop)

    def test_data_exists(self):
        DataFactory(
            date=datetime(2000, 1, 1).date(),
            distance=10.12,
            time=timedelta(seconds=15)
        )

        insert_data()

        data = models.Data.objects.all()

        self.assertEqual(1, data.count())

    def test_data_not_exists_1(self):
        DataFactory(
            date=datetime(1999, 1, 1).date(),
            distance=10.10,
            time=timedelta(seconds=15)
        )

        insert_data()

        data = models.Data.objects.order_by('-pk')

        self.assertEqual(2, data.count())

    def test_data_not_exists_2(self):
        DataFactory(
            date=datetime(2000, 1, 1).date(),
            distance=9.12345678,
            time=timedelta(seconds=15)
        )

        insert_data()

        data = models.Data.objects.order_by('-pk')

        self.assertEqual(2, data.count())

    def test_data_must_be_rounded(self):
        BikeFactory()

        insert_data()

        data = models.Data.objects.order_by('-pk')
        inserted_row = data[0]

        self.assertEqual(1, data.count())
        self.assertEqual(10.12, inserted_row.distance)


    def test_insert_data_redirection_if_user_not_logged(self):
            login_url = reverse('accounts:login')
            url = reverse('reports:insert_data')
            response = self.client.get(url)
            self.assertRedirects(response, '{login_url}?next={url}'.format(
                login_url=login_url, url=url))
