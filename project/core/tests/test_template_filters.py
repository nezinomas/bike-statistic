import pytest

from ..templatetags import template_filters as T


@pytest.mark.parametrize(
    'dictionary, key, expect',
    [
        ({'x': 'val'}, 'x', 'val'),
        ({'x': 'val'}, 'y', 0.0),
        (None, 'y', None),
        ({}, 'y', None),
    ])
def test_get_item(dictionary, key, expect):
    assert T.get_item(dictionary, key) == expect
