import pytest
from django.urls import resolve, reverse

from ..views import chart


@pytest.fixture(autouse=True)
def overall(monkeypatch):
    _cls = 'project.reports.views.chart.Overall.{}'
    monkeypatch.setattr(_cls.format('__init__'), lambda x: None)
    monkeypatch.setattr(_cls.format('bikes'), ['bike1',  'bike2'])
    monkeypatch.setattr(_cls.format('distances'), [[10, 20], [30, 40]])
    monkeypatch.setattr(_cls.format('years'), [2000, 2002])
    monkeypatch.setattr(
        _cls.format('totals_table'),
        {
            'columns': ['bike1', 'bike2'],
            'data': [[10, 20], [30, 40]],
            'index': [2000, 2002]
        }
    )
    monkeypatch.setattr(
        _cls.format('totals_grand'),
        {
            'columns': ['bike1', 'bike2'],
            'data': [[30, 60]],
            'index': ['Total']
        }
    )


def test_overall_chart_series(client):
    url = reverse('reports:overall')
    response = client.get(url)

    actual = response.context['chart']['overall']['series']

    assert 'bike2' == actual[0]['name']
    assert 'bike1' == actual[1]['name']

    assert [30, 40] == actual[0]['data']
    assert [10, 20] == actual[1]['data']


def test_overall_chart_xaxis(client):
    url = reverse('reports:overall')
    response = client.get(url)

    actual = response.context['chart']['overall']['xAxis']

    assert [2000, 2002] == actual


def test_overall_200(client):
    url = reverse('reports:overall')
    response = client.get(url)

    assert 200 == response.status_code


def test_overall_func():
    view = resolve('/reports/overall/')

    assert chart.overall == view.func
