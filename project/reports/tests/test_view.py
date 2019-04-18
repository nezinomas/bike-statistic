from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from .. import views
from ...core.factories import UserFactory


class TestDataTable(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory()

    def test_data_date_ok(self):
        self.client.login(username='bob', password='123')

        url = reverse(
            'reports:data_list',
            kwargs={
                'start_date': '2000-01-01',
                'end_date': '2000-01-31'
            }
        )
        response = self.client.get(url)

        self.assertContains(response, '<form class="filter"')

    def test_data_date_not_ok_01(self):
        response = self.client.get('/data/2000/2001/')
        self.assertEqual(response.status_code, 404)

    def test_data_date_not_ok_02(self):
        response = self.client.get('/data/xxxx-xx-xx/xxxx-xx-xx/')
        self.assertEqual(response.status_code, 404)

    def test_data_date_not_ok_03(self):
        response = self.client.get('/data/2000-99-99/9999-99-99/')
        self.assertEqual(response.status_code, 404)

    def test_data_view(self):
        view = resolve('/data/2000-01-01/2001-01-01/')
        self.assertEqual(view.func, views.data_list)


class TestDataTableEmptyDate(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory()

    def test_view_date_ok_01(self):
        self.client.login(username='bob', password='123')

        url = reverse('reports:data_empty')
        response = self.client.get(url, follow=True)

        self.assertContains(response, '<form class="filter"')

    def test_view(self):
        view = resolve('/data/')
        self.assertEqual(view.func, views.data_empty)


class TestDataTableNoEnd(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserFactory()

    def test_view_date_ok_01(self):
        self.client.login(username='bob', password='123')

        url = reverse(
            'reports:data_partial',
            kwargs={'start_date': '2000-01-01'}
        )
        response = self.client.get(url, follow=True)

        self.assertContains(response, '<form class="filter"')

    def test_view(self):
        view = resolve('/data/2000-01-01/')
        self.assertEqual(view.func, views.data_partial)
