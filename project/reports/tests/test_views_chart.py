import json

import pytest
from django.urls import resolve, reverse

from ..views import chart


@pytest.fixture()
def overall(monkeypatch):
    _cls = 'project.reports.views.chart.Overall.{}'
    monkeypatch.setattr(_cls.format('__init__'), lambda x: None)
    monkeypatch.setattr(_cls.format('bikes'), ['bike1',  'bike2'])
    monkeypatch.setattr(_cls.format('distances'), [[10, 20], [30, 40]])
    monkeypatch.setattr(_cls.format('years'), [2000, 2002])


def test_api_overall_200(client, overall):
    url = reverse('reports:api-overall')
    response = client.get(url)

    assert 200 == response.status_code


def test_api_everall_json_response_series(client, overall):
    url = reverse('reports:api-overall')
    response = client.get(url)

    content = json.loads(response.content)
    actual = content['overall']['series']

    assert 'bike2' == actual[0]['name']
    assert 'bike1' == actual[1]['name']

    assert [30, 40] == actual[0]['data']
    assert [10, 20] == actual[1]['data']


def test_api_everall_json_response_xaxis(client, overall):
    url = reverse('reports:api-overall')
    response = client.get(url)

    content = json.loads(response.content)
    actual = content['overall']['xAxis']

    assert [2000, 2002] == actual


def test_api_overall_func():
    view = resolve('/api/reports/overall/')

    assert chart.api_overall == view.func


def test_overall_200(client):
    url = reverse('reports:overall')
    response = client.get(url)

    assert 200 == response.status_code


def test_overall_func():
    view = resolve('/reports/overall/')

    assert chart.overall == view.func
