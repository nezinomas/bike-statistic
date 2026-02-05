import re
from datetime import date

import pytest
import time_machine
from django.urls import resolve, reverse

from ...bikes.factories import BikeFactory, ComponentFactory, ComponentWearFactory
from ...core.lib.tests_utils import clean_content
from .. import models, views

pytestmark = pytest.mark.django_db


def test_wear_list_func():
    view = resolve("/wear/bike/66/")

    assert views.ComponentWearList is view.func.view_class


def test_wear_create_func():
    view = resolve("/wear/bike/66/create/")

    assert views.ComponentWearCreate is view.func.view_class


def test_wear_update_func():
    view = resolve("/wear/bike/update/7/")

    assert views.ComponentWearUpdate is view.func.view_class


def test_wear_delete_func():
    view = resolve("/wear/bike/delete/7/")

    assert views.ComponentWearDelete is view.func.view_class


def test_wear_list_200(client_logged):
    bike = BikeFactory()
    component = ComponentFactory()
    url = reverse(
        "bikes:wear_list", kwargs={"bike_slug": bike.slug, "component_pk": component.pk}
    )
    response = client_logged.get(url)

    assert response.status_code == 200


def test_wear_list_alernative_200(client_logged):
    bike = BikeFactory()
    ComponentFactory()
    url = reverse("bikes:wear_list", kwargs={"bike_slug": bike.slug})
    response = client_logged.get(url)

    assert response.status_code == 200


def test_wear_list_no_component_200(client_logged):
    bike = BikeFactory()

    url = reverse("bikes:wear_list", kwargs={"bike_slug": bike.slug})
    response = client_logged.get(url)

    assert response.status_code == 200


def test_wear_list_no_data(client_logged):
    bike = BikeFactory()
    component = ComponentFactory()
    url = reverse(
        "bikes:wear_list", kwargs={"bike_slug": bike.slug, "component_pk": component.pk}
    )
    response = client_logged.get(url)
    content = clean_content(response.content)
    assert '<div class="alert alert-warning">No records</div>' in content


def test_wear_list_with_data(client_logged):
    bike = BikeFactory()
    component = ComponentFactory()
    ComponentWearFactory()

    url = reverse(
        "bikes:wear_list", kwargs={"bike_slug": bike.slug, "component_pk": component.pk}
    )
    response = client_logged.get(url)
    content = clean_content(response.content)

    assert "1999-01-01" in content
    assert "1999-01-31" in content
    assert "1,11" in content
    assert "Brand" in content


def test_wear_list_with_data_links(client_logged):
    bike = BikeFactory()
    component = ComponentFactory()
    stats = ComponentWearFactory()

    url = reverse(
        "bikes:wear_list", kwargs={"bike_slug": bike.slug, "component_pk": component.pk}
    )
    response = client_logged.get(url)
    actual = clean_content(response.content)

    url_update = reverse(
        "bikes:wear_update", kwargs={"bike_slug": bike.slug, "wear_pk": stats.pk}
    )
    url_delete = reverse(
        "bikes:wear_delete", kwargs={"bike_slug": bike.slug, "wear_pk": stats.pk}
    )

    # table row
    assert (
        f'<tr hx-target="#mainModal" hx-trigger="dblclick" hx-get="{url_update}"'
        in actual
    )
    # edit button
    assert (
        f'<button type="button" class="btn-secondary btn-edit" hx-get="{url_update}" hx-target="#mainModal"'  # noqa: E501
        in actual
    )
    # delete button
    assert (
        f'<button type="button" class="btn-trash" hx-get="{url_delete}" hx-target="#mainModal"'  # noqa: E501
        in actual
    )


def test_stats_rendered_context(client_logged):
    bike = BikeFactory()
    stats = ComponentWearFactory()

    url = reverse(
        "bikes:wear_list", kwargs={"bike_slug": bike.slug, "component_pk": stats.pk}
    )
    response = client_logged.get(url)

    actual = clean_content(response.content)

    url_update = reverse(
        "bikes:wear_update", kwargs={"bike_slug": bike.slug, "wear_pk": stats.pk}
    )
    url_delete = reverse(
        "bikes:wear_delete", kwargs={"bike_slug": bike.slug, "wear_pk": stats.pk}
    )

    # table row
    assert (
        f'<tr hx-target="#mainModal" hx-trigger="dblclick" hx-get="{url_update}"'
        in actual
    )
    # edit button
    assert (
        f'<button type="button" class="btn-secondary btn-edit" hx-get="{url_update}" hx-target="#mainModal" '  # noqa: E501
        in actual
    )
    # delete button
    assert (
        f'<button type="button" class="btn-trash" hx-get="{url_delete}" hx-target="#mainModal"'  # noqa: E501
        in actual
    )


@time_machine.travel("2000-02-02")
def test_wear_create_load_form(client_logged):
    bike = BikeFactory()
    component = ComponentFactory()

    url = reverse(
        "bikes:wear_create",
        kwargs={"bike_slug": bike.slug, "component_pk": component.pk},
    )
    response = client_logged.get(url)
    content = clean_content(response.content)

    assert '<select name="bike"' not in content
    assert '<select name="component"' not in content
    assert '<input type="text" name="start_date" value="2000-02-02"' in content


def test_wear_create_save_with_valid_data(client_logged):
    bike = BikeFactory()
    component = ComponentFactory()

    data = {
        "start_date": "2000-2-2",
        "end_date": "3000-3-3",
        "price": 6,
        "brand": "some brand",
    }

    url = reverse(
        "bikes:wear_create",
        kwargs={"bike_slug": bike.slug, "component_pk": component.pk},
    )
    client_logged.post(url, data)
    actual = models.ComponentWear.objects.first()

    assert actual.bike == bike
    assert actual.component == component
    assert actual.start_date == date(2000, 2, 2)
    assert actual.end_date == date(3000, 3, 3)
    assert actual.price == 6.0
    assert actual.brand == "some brand"


def test_wear_create_same_bike_another_component_not_closed(client_logged):
    bike = BikeFactory()
    component = ComponentFactory()
    ComponentWearFactory(
        bike=bike,
        component=ComponentFactory(name="Component 2"),
        start_date=date(1999, 1, 1),
        end_date=None,
    )

    data = {
        "start_date": "2000-2-2",
        "end_date": "3000-3-3",
        "price": 6,
        "brand": "some brand",
    }

    url = reverse(
        "bikes:wear_create",
        kwargs={"bike_slug": bike.slug, "component_pk": component.pk},
    )
    client_logged.post(url, data)

    actual = models.ComponentWear.objects.first()

    assert actual.bike == bike
    assert actual.component == component
    assert actual.start_date == date(2000, 2, 2)
    assert actual.end_date == date(3000, 3, 3)
    assert actual.price == 6.0
    assert actual.brand == "some brand"


def test_wear_create_another_bike_same_component_not_closed(client_logged):
    bike = BikeFactory()
    component = ComponentFactory()
    ComponentWearFactory(
        bike=BikeFactory(full_name="Bike 2", short_name="B2"),
        component=component,
        start_date=date(1999, 1, 1),
        end_date=None,
    )
    data = {
        "start_date": "2000-2-2",
        "end_date": "3000-3-3",
        "price": 6,
        "brand": "some brand",
    }

    url = reverse(
        "bikes:wear_create",
        kwargs={"bike_slug": bike.slug, "component_pk": component.pk},
    )
    client_logged.post(url, data)

    actual = models.ComponentWear.objects.first()

    assert actual.bike == bike
    assert actual.component == component
    assert actual.start_date == date(2000, 2, 2)
    assert actual.end_date == date(3000, 3, 3)
    assert actual.price == 6.0
    assert actual.brand == "some brand"


def test_wear_create_save_no_start_date(client_logged):
    bike = BikeFactory()
    component = ComponentFactory()

    data = {"start_date": "", "end_date": "3000-3-3", "price": 6, "brand": "some brand"}

    url = reverse(
        "bikes:wear_create",
        kwargs={"bike_slug": bike.slug, "component_pk": component.pk},
    )
    response = client_logged.post(url, data)
    form = response.context["form"]

    assert not form.is_valid()
    assert "start_date" in form.errors


def test_wear_update_load_form(client_logged):
    bike = BikeFactory()
    stats = ComponentWearFactory()

    url = reverse(
        "bikes:wear_update", kwargs={"bike_slug": bike.slug, "wear_pk": stats.pk}
    )
    response = client_logged.get(url)
    form = response.context["form"].as_p()

    assert "1999-01-01" in form
    assert "1999-01-31" in form
    assert "1.11" in form
    assert "Brand" in form


def test_wear_update_load_form_close_button(client_logged):
    bike = BikeFactory()
    stats = ComponentWearFactory()

    url = reverse(
        "bikes:wear_list", kwargs={"bike_slug": bike.slug, "component_pk": stats.pk}
    )
    response = client_logged.get(url)
    actual = clean_content(response.content)

    url_close = reverse(
        "bikes:wear_update", kwargs={"bike_slug": bike.slug, "wear_pk": stats.pk}
    )
    assert f'hx-get="{url_close}"' in actual


def test_wear_update_start_date(client_logged):
    bike = BikeFactory()
    stats = ComponentWearFactory()

    data = {
        "start_date": "1999-1-30",
        "end_date": str(stats.end_date),
        "price": stats.price,
        "brand": stats.brand,
    }

    url = reverse(
        "bikes:wear_update", kwargs={"bike_slug": bike.slug, "wear_pk": stats.pk}
    )
    client_logged.post(url, data)

    actual = models.ComponentWear.objects.get(pk=stats.pk)

    assert actual.start_date == date(1999, 1, 30)


def test_wear_update_end_date(client_logged):
    bike = BikeFactory()
    stats = ComponentWearFactory()

    data = {
        "start_date": str(stats.start_date),
        "price": stats.price,
        "brand": stats.brand,
    }

    url = reverse(
        "bikes:wear_update", kwargs={"bike_slug": bike.slug, "wear_pk": stats.pk}
    )
    client_logged.post(url, data)

    actual = models.ComponentWear.objects.get(pk=stats.pk)

    assert not actual.end_date


def test_wear_update_brand_no_end_date(client_logged):
    obj = ComponentWearFactory(end_date=None)

    obj.brand = "Brand New"

    data = {
        "start_date": str(obj.start_date),
        "end_date": "",
        "price": obj.price,
        "brand": obj.brand,
        "component": obj.component.pk,
        "bike": obj.bike.pk,
    }

    url = reverse(
        "bikes:wear_update", kwargs={"bike_slug": obj.bike.slug, "wear_pk": obj.pk}
    )
    client_logged.post(url, data)

    actual = models.ComponentWear.objects.get(pk=obj.pk)

    assert actual.brand == "Brand New"


def test_wear_delete_200(client_logged):
    bike = BikeFactory()
    stats = ComponentWearFactory()
    url = reverse(
        "bikes:wear_delete", kwargs={"bike_slug": bike.slug, "wear_pk": stats.pk}
    )

    response = client_logged.get(url)

    assert response.status_code == 200


def test_wear_delete_load_form(client_logged):
    bike = BikeFactory()
    stats = ComponentWearFactory()
    url = reverse(
        "bikes:wear_delete", kwargs={"bike_slug": bike.slug, "wear_pk": stats.pk}
    )

    response = client_logged.get(url)
    content = clean_content(response.content)

    res = re.findall(rf'<form.+hx-post="({url})"', content)
    assert res[0] == url
    assert f'<button type="submit" id="_delete" data-pk="{stats.pk}"' in content


def test_wear_delete(client_logged):
    bike = BikeFactory()
    stats = ComponentWearFactory()
    url = reverse(
        "bikes:wear_delete", kwargs={"bike_slug": bike.slug, "wear_pk": stats.pk}
    )

    client_logged.post(url, {})

    assert models.ComponentWear.objects.all().count() == 0
