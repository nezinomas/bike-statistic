from django.test import TestCase

from ..library.chart import get_color, colors


class GetColorTests(TestCase):
    def test_num_bigger(self):
        last = len(colors)-1
        expected = 'rgba({r}, {g}, {b}, 5)'.format(
            r=colors[last][0], g=colors[last][1], b=colors[last][2])

        actual = get_color(100, 5)

        self.assertEqual(actual, expected)
