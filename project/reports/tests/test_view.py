from django.test import TestCase
from django.urls import reverse, resolve, reverse_lazy
from django.contrib.auth.models import User

from .. import views

class TestDataTable(TestCase):
    @classmethod
    def setUpTestData(cls):
        u = 'bob'
        p = '123'
        e = 'bob@bob.com'

        User.objects.create_user(username=u, password=p, email=e)

    def test_view_date_ok_01(self):
        self.client.login(username='bob', password='123')
        url = reverse(
            'reports:data_table',
            kwargs={
                'start_date': '2000-01-01',
                'end_date': '2000-01-31'
            }
        )
        response = self.client.get(url)

        self.assertContains(response, '<form  class="data"')
        self.assertContains(response, '<form  class="filter"')

    # def test_view_date_ok_02(self):
    #     url = reverse(
    #         'reports:data_table',
    #         kwargs={
    #             'start_date': '2000-1-1',
    #             'end_date': '2000-1-1'
    #         }
    #     )
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)

    def test_view_date_not_ok_01(self):
        response = self.client.get('/data/2000/2001')
        self.assertEqual(response.status_code, 404)

    def test_view_date_not_ok_02(self):
        response = self.client.get('/data/xxxx-xx-xx/xxxx-xx-xx')
        self.assertEqual(response.status_code, 404)

    def test_view_date_not_ok_03(self):
        # url = reverse_lazy(
        #     'reports:data_table',
        #     kwargs={
        #         'start_date': '2000-xx-xx',
        #         'end_date': '2000-01-11'
        #     }
        # )
        # response = self.client.get(url)
        response = self.client.get('/data/2000-99-99/9999-99-99/')
        self.assertEqual(response.status_code, 404)

    def test_view(self):
        view = resolve('/data/2000-01-01/2001-01-01')
        self.assertEqual(view.func, views.data_table)


class TestDataTableEmptyDate(TestCase):
    @classmethod
    def setUpTestData(cls):
        u = 'bob'
        p = '123'
        e = 'bob@bob.com'

        User.objects.create_user(username=u, password=p, email=e)

    def test_view_date_ok_01(self):
        url = reverse('reports:data_table_empty_date')
        self.client.login(username='bob', password='123')

        response = self.client.get(url, follow=True)

        self.assertContains(response, '<form  class="data"')
        self.assertContains(response, '<form  class="filter"')

    def test_view(self):
        view = resolve('/data/')
        self.assertEqual(view.func, views.data_table_empty_date)


class TestDataTableNoEnd(TestCase):
    @classmethod
    def setUpTestData(cls):
        u = 'bob'
        p = '123'
        e = 'bob@bob.com'

        User.objects.create_user(username=u, password=p, email=e)

    def test_view_date_ok_01(self):
        url = reverse(
            'reports:data_table_no_end',
            kwargs={'start_date': '2000-01-01'}
        )
        self.client.login(username='bob', password='123')
        response = self.client.get(url, follow=True)

        self.assertContains(response, '<form  class="data"')
        self.assertContains(response, '<form  class="filter"')

    def test_view(self):
        view = resolve('/data/2000-01-01/')
        self.assertEqual(view.func, views.data_table_no_end)


class TestInsertData(TestCase):
    pass
