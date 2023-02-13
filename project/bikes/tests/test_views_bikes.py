import re
from datetime import date

import pytest
import time_machine
from django.urls import resolve, reverse

from ...bikes.factories import BikeFactory, ComponentFactory
from ...core.lib.tests_utils import clean_content
from ...users.factories import UserFactory
from .. import models, views

pytestmark = pytest.mark.django_db


def test_bike_list_func():
    view = resolve('/bike/')

    assert views.BikeList is view.func.view_class


def test_bike_detail_func():
    view = resolve('/bike/detail/9/')

    assert views.BikeDetail is view.func.view_class


def test_bike_create_func():
    view = resolve('/bike/create/')

    assert views.BikeCreate is view.func.view_class


def test_bike_update_func():
    view = resolve('/bike/update/1/')

    assert views.BikeUpdate is view.func.view_class


def test_bike_delete_func():
    view = resolve('/bike/delete/1/')

    assert views.BikeDelete is view.func.view_class


def test_bike_list_200(client_logged):
    url = reverse('bikes:bike_list')
    response = client_logged.get(url)

    assert response.status_code == 200


def test_bike_list_no_records(client_logged):
    url = reverse('bikes:bike_list')
    response = client_logged.get(url)

    assert '<td class="bg-warning text-center" colspan="4"> No records </td>' in str(
        response.content)


def test_bike_list(client_logged):
    bike = BikeFactory()

    url = reverse('bikes:bike_list')
    response = client_logged.get(url)
    content = clean_content(response.content)
    info_url = reverse("bikes:info_list", kwargs={"bike_slug": bike.slug})

    assert '1999-01-01' in content
    assert 'Full Name' in content
    assert f'<a href="{info_url}">Short Name</a>' in content


def test_bike_detail(client_logged):
    bike = BikeFactory()

    url = reverse('bikes:bike_detail', kwargs={'pk': bike.pk})
    response = client_logged.get(url)

    actual = response.context['object']
    assert response.status_code == 200
    assert actual == bike


def test_bike_detail_links(client_logged):
    bike = BikeFactory()

    url = reverse('bikes:bike_detail', kwargs={'pk': bike.pk})
    response = client_logged.get(url)

    actual = clean_content(response.content)

    row_id = f'row-id-{bike.pk}'
    url_update = reverse('bikes:bike_update', kwargs={'pk': bike.pk})
    url_delete = reverse('bikes:bike_delete', kwargs={'pk': bike.pk})

    # table row
    assert f'<tr id="{row_id}" hx-target="this" hx-swap="outerHTML" hx-trigger="click[ctrlKey]" hx-get="{url_update}">' in actual
    # edit button
    assert f'<button type="button" class="btn btn-sm btn-warning" hx-get="{url_update}" hx-target="#{row_id}" hx-swap="outerHTML">' in actual
    # delete button
    assert f'<button type="button" class="btn btn-sm btn-danger" hx-get="{url_delete}" hx-target="#dialog" hx-swap="innerHTML">' in actual


@time_machine.travel('2000-2-2')
def test_bike_create_load_form(client_logged):
    url = reverse('bikes:bike_create')
    response = client_logged.get(url)
    content = clean_content(response.content)

    assert response.status_code == 200
    assert '<input type="text" name="date" value="2000-02-02"' in content


def test_bike_create_save_with_valid_data(client_logged):
    user = UserFactory()

    data = {
        'date': '2000-2-2',
        'full_name': 'Full Name',
        'short_name': 'Short Name',
        'main': 'True'
    }

    url = reverse('bikes:bike_create')
    client_logged.post(url, data)
    actual = models.Bike.objects.first()

    assert actual.date == date(2000, 2, 2)
    assert actual.full_name == 'Full Name'
    assert actual.short_name == 'Short Name'
    assert actual.user == user
    assert actual.main is True
    assert actual.retired is False


def test_bike_create_save_form_errors(client_logged):
    data = {}
    url = reverse('bikes:bike_create')
    response = client_logged.post(url, data)
    form = response.context['form']
    assert not form.is_valid()
    assert 'date' in form.errors
    assert 'short_name' in form.errors


def test_bike_update_load_form(client_logged):
    bike = BikeFactory()

    url = reverse('bikes:bike_update', kwargs={'pk': bike.pk})
    response = client_logged.get(url)
    form = response.context['form'].as_p()

    assert '1999-01-01' in form
    assert 'Full Name' in form
    assert 'Short Name' in form


def test_bike_update_load_form_close_button(client_logged):
    bike = BikeFactory()

    url = reverse('bikes:bike_update', kwargs={'pk': bike.pk})
    response = client_logged.get(url)
    actual = clean_content(response.content)

    url_close = reverse('bikes:bike_detail', kwargs={'pk': bike.pk})
    assert f'hx-get="{url_close}"' in actual


def test_bike_update_date(client_logged):
    bike = BikeFactory()

    data = {
        'date': '1999-1-30',
        'full_name': bike.full_name,
        'short_name': bike.short_name,
        'main': bike.main,
        'retired': bike.retired,
    }

    url = reverse('bikes:bike_update', kwargs={'pk': bike.pk})
    client_logged.post(url, data)

    actual = models.Bike.objects.get(pk=bike.pk)

    assert actual.date == date(1999, 1, 30)
    assert actual.full_name == bike.full_name
    assert actual.short_name == bike.short_name
    assert actual.main == bike.main
    assert actual.retired == bike.retired


def test_bike_update_full_name(client_logged):
    bike = BikeFactory()

    data = {
        'date': str(bike.date),
        'full_name': 'XXX',
        'short_name': bike.short_name,
        'main': bike.main,
        'retired': bike.retired,
    }

    url = reverse('bikes:bike_update', kwargs={'pk': bike.pk})
    client_logged.post(url, data)

    actual = models.Bike.objects.get(pk=bike.pk)

    assert actual.date == bike.date
    assert actual.full_name == 'XXX'
    assert actual.short_name == bike.short_name
    assert actual.main == bike.main
    assert actual.retired == bike.retired


def test_bike_update_short_name(client_logged):
    bike = BikeFactory()

    data = {
        'date': str(bike.date),
        'full_name': bike.full_name,
        'short_name': 'xxx',
        'main': bike.main,
        'retired': bike.retired,
    }

    url = reverse('bikes:bike_update', kwargs={'pk': bike.pk})
    client_logged.post(url, data)

    actual = models.Bike.objects.get(pk=bike.pk)

    assert actual.date == bike.date
    assert actual.full_name == bike.full_name
    assert actual.short_name == 'xxx'
    assert actual.main == bike.main
    assert actual.retired == bike.retired


def test_bike_update_main(client_logged):
    bike = BikeFactory()

    data = {
        'date': str(bike.date),
        'full_name': bike.full_name,
        'short_name': bike.short_name,
        'main': True,
        'retired': bike.retired,
    }

    url = reverse('bikes:bike_update', kwargs={'pk': bike.pk})
    client_logged.post(url, data)

    actual = models.Bike.objects.get(pk=bike.pk)

    assert actual.date == bike.date
    assert actual.full_name == bike.full_name
    assert actual.short_name == bike.short_name
    assert actual.main is True
    assert actual.retired == bike.retired


def test_bike_update_retired(client_logged):
    bike = BikeFactory()

    data = {
        'date': str(bike.date),
        'full_name': bike.full_name,
        'short_name': bike.short_name,
        'main': bike.main,
        'retired': True,
    }

    url = reverse('bikes:bike_update', kwargs={'pk': bike.pk})
    client_logged.post(url, data)

    actual = models.Bike.objects.get(pk=bike.pk)

    assert actual.date == bike.date
    assert actual.full_name == bike.full_name
    assert actual.short_name == bike.short_name
    assert actual.main == bike.main
    assert actual.retired is True


def test_bike_delete_200(client_logged):
    bike = BikeFactory()
    url = reverse('bikes:bike_delete', kwargs={'pk': bike.pk})

    response = client_logged.get(url)

    assert response.status_code == 200


def test_bike_delete_load_form(client_logged):
    bike = BikeFactory()
    url = reverse('bikes:bike_delete', kwargs={'pk': bike.pk})

    response = client_logged.get(url)
    content = clean_content(response.content)

    res = re.findall(fr'<form.+hx-post="({url})"', content)
    assert res[0] == url
    assert f'<button type="submit" id="_delete" data-pk="{bike.pk}"' in content


def test_bike_delete(client_logged):
    bike = BikeFactory()
    url = reverse('bikes:bike_delete', kwargs={'pk': bike.pk})

    client_logged.post(url, {})

    assert models.Bike.objects.all().count() == 0


def test_bike_menu_func():
    view = resolve('/bike/menu/')

    assert views.BikeMenuList is view.func.view_class


def test_bike_menu_200(client_logged):
    url = reverse('bikes:bike_menu')
    response = client_logged.get(url)

    assert response.status_code == 200


def test_bike_menu(client_logged):
    bike = BikeFactory()
    component = ComponentFactory()

    url = reverse('bikes:bike_menu')
    response = client_logged.get(url)
    content = clean_content(response.content)
    stats_url = reverse("bikes:stats_list", kwargs={"bike_slug": bike.slug, "component_pk": component.pk})

    assert f'hx-get="{stats_url}"> Short Name </a>' in content
