from django.test import TestCase
from django.urls import reverse, resolve

from .. import views, models
from .. endomondo import Workout


class GetDataTests(TestCase):
    def test_view_status_code_200(self):
        url = reverse('reports:get_data')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_func(self):
        view = resolve('/data/get')
        self.assertEqual(view.func, views.get_data)
