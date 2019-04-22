from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import resolve, reverse
from mock import patch

from .. import models, views
from ..endomondo import Workout
from ...core.factories import BikeFactory, DataFactory, UserFactory
from ..library.insert_data import insert_data


class GetDataViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory()

    def test_view_status_code_200(self):
        self.client.login(username='bob', password='123')

        url = reverse('reports:insert_data')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_view_func(self):
        view = resolve('/data/insert/')
        self.assertEqual(view.func, views.insert_data)

    def test_insert_data_redirection_if_user_not_logged(self):
            login_url = reverse('accounts:login')
            url = reverse('reports:insert_data')
            response = self.client.get(url)
            self.assertRedirects(response, '{login_url}?next={url}'.format(
                login_url=login_url, url=url))
