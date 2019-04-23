import pytest
from mock import patch

from ..library import chart


@patch('project.reports.library.chart.colors', [(1, 1, 1)])
def test_num_bigger():
    expected = 'rgba(1, 1, 1, 5)'
    actual = chart.get_color(100, 5)

    assert expected == actual
