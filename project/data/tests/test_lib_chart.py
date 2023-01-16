from mock import patch

from ..library import chart


@patch('project.data.library.chart.colors', [(1, 1, 1)])
def test_num_bigger():
    expected = 'rgba(1, 1, 1, 5)'
    actual = chart.get_color(100, 5)

    assert expected == actual

@patch('project.data.library.chart.colors', [(1, 1, 1), (2, 2, 2)])
def test_num_equal_to_color_list():
    expected = 'rgba(2, 2, 2, 5)'
    actual = chart.get_color(2, 5)

    assert expected == actual
