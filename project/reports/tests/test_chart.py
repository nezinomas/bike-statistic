from mock import patch

from django.test import TestCase

from ..library import chart


@patch('project.reports.library.chart.colors', [(1, 1, 1)])
class GetColorTests(TestCase):

    def test_num_bigger(self):
        expected = 'rgba(1, 1, 1, 5)'

        actual = chart.get_color(100, 5)

        self.assertEqual(actual, expected)
