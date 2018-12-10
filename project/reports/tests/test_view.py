from django.test import TestCase
from django.urls import reverse, resolve, reverse_lazy

from .. import views

class TestDataTable(TestCase):

    def test_view_date_ok_01(self):
        url = reverse(
            'reports:data_table',
            kwargs={
                'start_date': '2000-01-01',
                'end_date': '2000-01-01'
            }
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

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
    def test_view_date_ok_01(self):
        url = reverse('reports:data_table_empty_date')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view(self):
        view = resolve('/data/')
        self.assertEqual(view.func, views.data_table_empty_date)


class TestDataTableNoEnd(TestCase):
    def test_view_date_ok_01(self):
        url = reverse(
            'reports:data_table_no_end',
            kwargs={'start_date': '2000-01-01'}
        )
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view(self):
        view = resolve('/data/2000-01-01/')
        self.assertEqual(view.func, views.data_table_no_end)


class TestInsertData(TestCase):
    pass

