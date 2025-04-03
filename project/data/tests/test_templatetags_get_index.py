import pytest

from ..templatetags.get_index import get_index


@pytest.fixture()
def years():
    return [2000, 2001]


@pytest.fixture()
def distances():
    return [[1.1, 1.2], [2.1, 2.2, 2.3]]


def test_get_index_01(distances):
    actual = get_index(distances, 1)

    assert [2.1, 2.2, 2.3] == actual
