import re
from datetime import date

import pytest
from django.urls import resolve, reverse

from ...bikes.factories import (BikeFactory, ComponentFactory,
                                ComponentStatisticFactory)
from ...core.lib.tests_utils import clean_content
from .. import models, views

pytestmark = pytest.mark.django_db


def test_stats_detail_func():
    view = resolve('/stats/bike/detail/9/')

    assert views.StatsDetail is view.func.view_class


def test_stats_list_func():
    view = resolve('/stats/bike/66/')

    assert views.StatsList is view.func.view_class


def test_stats_create_func():
    view = resolve('/stats/bike/66/create/')

    assert views.StatsCreate is view.func.view_class


def test_stats_update_func():
    view = resolve('/stats/bike/update/7/')

    assert views.StatsUpdate is view.func.view_class


def test_stats_delete_func():
    view = resolve('/stats/bike/delete/7/')

    assert views.StatsDelete is view.func.view_class


def test_stats_list_200(client_logged):
    bike = BikeFactory()
    component = ComponentFactory()
    url = reverse('bikes:stats_list', kwargs={'bike_slug': bike.slug, 'component_pk': component.pk})
    response = client_logged.get(url)

    assert response.status_code == 200


def test_stats_list_no_data(client_logged):
    bike = BikeFactory()
    component = ComponentFactory()
    url = reverse('bikes:stats_list', kwargs={'bike_slug': bike.slug, 'component_pk': component.pk})
    response = client_logged.get(url)
    content = clean_content(response.content)
    assert '<td class="bg-warning text-center" colspan="6">No records</td>' in content


def test_stats_list_with_data(client_logged):
    bike = BikeFactory()
    component = ComponentFactory()
    ComponentStatisticFactory()

    url = reverse('bikes:stats_list', kwargs={'bike_slug': bike.slug, 'component_pk': component.pk})
    response = client_logged.get(url)
    content = clean_content(response.content)

    assert '1999-01-01' in content
    assert '1999-01-31' in content
    assert '1.11' in content
    assert 'Brand' in content


def test_stats_list_with_data_links(client_logged):
    bike = BikeFactory()
    component = ComponentFactory()
    stats = ComponentStatisticFactory()

    url = reverse('bikes:stats_list', kwargs={'bike_slug': bike.slug, 'component_pk': component.pk})
    response = client_logged.get(url)
    actual = clean_content(response.content)

    row_id = f'row-id-{stats.pk}'
    url_update = reverse('bikes:stats_update', kwargs={'bike_slug': bike.slug, 'stats_pk': stats.pk})
    url_delete = reverse('bikes:stats_delete', kwargs={'bike_slug': bike.slug, 'stats_pk': stats.pk})

    # table row
    assert f'<tr id="{row_id}" hx-target="this" hx-swap="outerHTML" hx-trigger="click[ctrlKey]" hx-get="{url_update}">' in actual
    # edit button
    assert f'<button type="button" class="btn btn-sm btn-warning" hx-get="{url_update}" hx-target="#{row_id}" hx-swap="outerHTML">' in actual
    # delete button
    assert f'<button type="button" class="btn btn-sm btn-danger" hx-get="{url_delete}" hx-target="#dialog" hx-swap="innerHTML">' in actual


def test_stats_detail(client_logged):
    bike = BikeFactory()
    stats = ComponentStatisticFactory()

    url = reverse('bikes:stats_detail', kwargs={'bike_slug': bike.slug, 'stats_pk': stats.pk})
    response = client_logged.get(url)

    actual = response.context['object']
    assert actual == stats


def test_stats_detail_rendered_context(client_logged):
    bike = BikeFactory()
    stats = ComponentStatisticFactory()

    url = reverse('bikes:stats_detail', kwargs={'bike_slug': bike.slug, 'stats_pk': stats.pk})
    response = client_logged.get(url)

    actual = clean_content(response.content)

    row_id = f'row-id-{stats.pk}'
    url_update = reverse('bikes:stats_update', kwargs={'bike_slug': bike.slug, 'stats_pk': stats.pk})
    url_delete = reverse('bikes:stats_delete', kwargs={'bike_slug': bike.slug, 'stats_pk': stats.pk})

    # table row
    assert f'<tr id="{row_id}" hx-target="this" hx-swap="outerHTML" hx-trigger="click[ctrlKey]" hx-get="{url_update}">' in actual
    # edit button
    assert f'<button type="button" class="btn btn-sm btn-warning" hx-get="{url_update}" hx-target="#{row_id}" hx-swap="outerHTML">' in actual
    # delete button
    assert f'<button type="button" class="btn btn-sm btn-danger" hx-get="{url_delete}" hx-target="#dialog" hx-swap="innerHTML">' in actual


@pytest.mark.freeze_time('2000-2-2')
def test_stats_create_load_form(client_logged):
    bike = BikeFactory()
    component = ComponentFactory()

    url = reverse('bikes:stats_create', kwargs={'bike_slug': bike.slug, 'component_pk': component.pk})
    response = client_logged.get(url)
    content = clean_content(response.content)

    assert '<select name="bike"' not in content
    assert '<select name="component"' not in content
    assert '<input type="text" name="start_date" value="2000-02-02"' in content


def test_stats_create_save_with_valid_data(client_logged):
    bike = BikeFactory()
    component = ComponentFactory()

    data = {
        'start_date': '2000-2-2',
        'end_date': '3000-3-3',
        'price': 6,
        'brand': 'some brand'
    }

    url = reverse('bikes:stats_create', kwargs={'bike_slug': bike.slug, 'component_pk': component.pk})
    client_logged.post(url, data)
    actual = models.ComponentStatistic.objects.first()

    assert actual.bike == bike
    assert actual.component == component
    assert actual.start_date == date(2000, 2, 2)
    assert actual.end_date == date(3000, 3, 3)
    assert actual.price == 6.0
    assert actual.brand == 'some brand'


def test_stats_create_save_no_start_date(client_logged):
    bike = BikeFactory()
    component = ComponentFactory()

    data = {
        'start_date': '',
        'end_date': '3000-3-3',
        'price': 6,
        'brand': 'some brand'
    }

    url = reverse('bikes:stats_create', kwargs={'bike_slug': bike.slug, 'component_pk': component.pk})
    response = client_logged.post(url, data)
    form = response.context['form']

    assert not form.is_valid()
    assert 'start_date' in form.errors


def test_stats_update_load_form(client_logged):
    bike = BikeFactory()
    stats = ComponentStatisticFactory()

    url = reverse('bikes:stats_update', kwargs={'bike_slug': bike.slug, 'stats_pk': stats.pk})
    response = client_logged.get(url)
    form = response.context['form'].as_p()

    assert '1999-01-01' in form
    assert '1999-01-31' in form
    assert '1.11' in form
    assert 'Brand' in form


def test_stats_update_load_form_close_button(client_logged):
    bike = BikeFactory()
    stats = ComponentStatisticFactory()

    url = reverse('bikes:stats_detail', kwargs={'bike_slug': bike.slug, 'stats_pk': stats.pk})
    response = client_logged.get(url)
    actual = clean_content(response.content)

    url_close = reverse('bikes:stats_update', kwargs={'bike_slug': bike.slug, 'stats_pk': stats.pk})
    assert f'hx-get="{url_close}"' in actual


def test_stats_update_start_date(client_logged):
    bike = BikeFactory()
    stats = ComponentStatisticFactory()

    data = {
        'start_date': '1999-1-30',
        'end_date': str(stats.end_date),
        'price': stats.price,
        'brand': stats.brand
    }

    url = reverse('bikes:stats_update', kwargs={'bike_slug': bike.slug, 'stats_pk': stats.pk})
    client_logged.post(url, data)

    actual = models.ComponentStatistic.objects.get(pk=stats.pk)

    assert actual.start_date == date(1999, 1, 30)


def test_stats_update_end_date(client_logged):
    bike = BikeFactory()
    stats = ComponentStatisticFactory()

    data = {
        'start_date': str(stats.start_date),
        'price': stats.price,
        'brand': stats.brand
    }

    url = reverse('bikes:stats_update', kwargs={'bike_slug': bike.slug, 'stats_pk': stats.pk})
    client_logged.post(url, data)

    actual = models.ComponentStatistic.objects.get(pk=stats.pk)

    assert not actual.end_date


def test_stats_delete_200(client_logged):
    bike = BikeFactory()
    stats = ComponentStatisticFactory()
    url = reverse('bikes:stats_delete', kwargs={'bike_slug': bike.slug, 'stats_pk': stats.pk})

    response = client_logged.get(url)

    assert response.status_code == 200


def test_stats_delete_load_form(client_logged):
    bike = BikeFactory()
    stats = ComponentStatisticFactory()
    url = reverse('bikes:stats_delete', kwargs={'bike_slug': bike.slug, 'stats_pk': stats.pk})

    response = client_logged.get(url)
    content = clean_content(response.content)

    res = re.findall(fr'<form.+hx-post="({url})"', content)
    assert res[0] == url
    assert f'<button type="submit" id="_delete" data-pk="{stats.pk}"' in content


def test_stats_delete(client_logged):
    bike = BikeFactory()
    stats = ComponentStatisticFactory()
    url = reverse('bikes:stats_delete', kwargs={'bike_slug': bike.slug, 'stats_pk': stats.pk})

    client_logged.post(url, {})

    assert models.ComponentStatistic.objects.all().count() == 0
