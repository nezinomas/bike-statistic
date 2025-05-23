import re
from datetime import date, datetime, timedelta, timezone

import pytest
import time_machine
from django.urls import resolve, reverse

from ...bikes.factories import BikeFactory
from ...core.lib.tests_utils import clean_content
from ...data.factories import DataFactory
from ...users.factories import UserFactory
from ...users.views import Login
from .. import views
from ..factories import DataFactory
from ..models import Data

pytestmark = pytest.mark.django_db


@time_machine.travel("2000-1-1")
def test_data_links(client_logged):
    data = DataFactory()

    url = reverse("data:data_list")
    response = client_logged.get(url)

    actual = clean_content(response.content)

    row_id = f"row-id-{data.pk}"
    url_update = reverse("data:data_update", kwargs={"pk": data.pk})
    url_delete = reverse("data:data_delete", kwargs={"pk": data.pk})
    url_quick_update = reverse("data:data_quick_update", kwargs={"pk": data.pk})

    # table row
    assert (
        f'<tr id="{row_id}" class="waiting-for-review" hx-target="#mainModal" hx-trigger="dblclick" hx-get="{url_update}"'  # noqa: E501
        in actual
    )
    # quick save button
    assert (
        f'<button type="button" class="btn-save" hx-get="{url_quick_update}" hx-target="#{row_id}" hx-swap="outerHTML"'  # noqa: E501
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


def test_data_list_func():
    view = resolve("/data/list/")

    assert views.DataList is view.func.view_class


def test_data_list_not_loged(client):
    url = reverse("data:data_list")
    response = client.get(url, follow=True)

    assert response.resolver_match.func.view_class is Login


@time_machine.travel("2000-01-20")
def test_data_list_user_items(client_logged):
    DataFactory()
    DataFactory(user=UserFactory(username="xxx"))

    url = reverse("data:data_list")

    response = client_logged.get(url)

    assert len(response.context["object_list"]) == 1
    assert response.context["object_list"][0].user.username == "bob"


def test_data_create_func():
    view = resolve("/data/create/")

    assert views.DataCreate is view.func.view_class


def test_data_create_not_loged(client):
    url = reverse("data:data_create")
    response = client.get(url, follow=True)
    assert response.resolver_match.func.view_class is Login


@time_machine.travel(datetime(2000, 2, 2, 5, 6, 7, tzinfo=timezone.utc))
def test_data_create_load_form(client_logged):
    url = reverse("data:data_create")
    response = client_logged.get(url)
    content = clean_content(response.content)

    assert response.status_code == 200
    assert '<input type="text" name="date" value="2000-02-02 05:06:07"' in content


@time_machine.travel("2000-1-1")
def test_data_create_data_valid(client_logged):
    bike = BikeFactory()
    data = {
        "bike": str(bike.id),
        "date": datetime(2000, 1, 1, 3, 2, 1),
        "distance": 10.12,
        "time": timedelta(seconds=15),
        "temperature": 1.1,
        "ascent": 600,
        "descent": 500,
        "max_speed": 110,
        "cadence": 120,
        "heart_rate": 200,
    }
    url = reverse("data:data_create")
    client_logged.post(url, data=data)

    actual = Data.objects.first()

    assert actual.date == datetime(2000, 1, 1, 3, 2, 1, tzinfo=timezone.utc)
    assert actual.distance == 10.12
    assert actual.time == timedelta(seconds=15)
    assert actual.temperature == 1.1
    assert actual.ascent == 600
    assert actual.descent == 500
    assert actual.max_speed == 110
    assert actual.cadence == 120
    assert actual.heart_rate == 200


def test_data_create_data_valid_db_object(client_logged, get_user):
    bike = BikeFactory()
    data = {
        "bike": str(bike.id),
        "date": datetime(2000, 1, 1, 3, 2, 1),
        "distance": 10.12,
        "time": timedelta(seconds=15),
        "temperature": 1.1,
        "ascent": 600,
        "descent": 500,
        "max_speed": 110,
        "cadence": 120,
        "heart_rate": 200,
    }
    url = reverse("data:data_create")
    client_logged.post(url, data=data)

    actual = Data.objects.first()

    assert actual.user == get_user
    assert actual.bike == bike
    assert actual.date == datetime(2000, 1, 1, 3, 2, 1, tzinfo=timezone.utc)
    assert actual.distance == 10.12
    assert actual.time == timedelta(seconds=15)
    assert actual.temperature == 1.1
    assert actual.ascent == 600
    assert actual.descent == 500
    assert actual.max_speed == 110
    assert actual.cadence == 120
    assert actual.heart_rate == 200


def test_data_create_data_invalid(client_logged):
    url = reverse("data:data_create")
    response = client_logged.post(url, data={})

    form = response.context["form"]
    assert not form.is_valid()
    assert "bike" in form.errors
    assert "date" in form.errors
    assert "distance" in form.errors
    assert "time" in form.errors


def test_data_delete_func():
    view = resolve("/data/delete/1/")

    assert views.DataDelete is view.func.view_class


def test_data_delete_not_loged(client):
    data = DataFactory()
    url = reverse("data:data_delete", kwargs={"pk": data.pk})
    response = client.get(url, follow=True)
    assert response.resolver_match.func.view_class is Login


def test_data_delete_200(client_logged):
    data = DataFactory()
    url = reverse("data:data_delete", kwargs={"pk": data.pk})

    response = client_logged.get(url)

    assert response.status_code == 200


def test_data_delete_404(client_logged):
    url = reverse("data:data_delete", kwargs={"pk": 99})
    response = client_logged.post(url)

    assert response.status_code == 404


def test_data_delete_load_form(client_logged):
    data = DataFactory()
    url = reverse("data:data_delete", kwargs={"pk": data.pk})

    response = client_logged.get(url)
    content = clean_content(response.content)

    res = re.findall(rf'<form.+hx-post="({url})"', content)
    assert res[0] == url
    assert f'<button type="submit" id="_delete" data-pk="{data.pk}"' in content


def test_data_delete(client_logged):
    obj = DataFactory()

    url = reverse("data:data_delete", kwargs={"pk": obj.pk})
    client_logged.post(url, {})

    assert Data.objects.all().count() == 0


def test_data_update_func():
    view = resolve("/data/update/1/")

    assert views.DataUpdate is view.func.view_class


def test_data_update_not_loged(client):
    data = DataFactory()
    url = reverse("data:data_update", kwargs={"pk": data.pk})
    response = client.get(url, follow=True)
    assert response.resolver_match.func.view_class is Login


def test_data_update_object_200(client_logged):
    data = DataFactory()
    url = reverse("data:data_update", kwargs={"pk": data.pk})
    response = client_logged.get(url)

    assert response.status_code == 200


def test_data_update_object_404(client_logged):
    url = reverse("data:data_update", kwargs={"pk": 99})
    response = client_logged.get(url)

    assert response.status_code == 404


def test_data_update_loaded_form(client_logged):
    obj = DataFactory()
    url = reverse("data:data_update", kwargs={"pk": obj.pk})
    response = client_logged.get(url)
    content = clean_content(response.content)

    assert f'<option value="{obj.bike.pk}" selected>Short Name</option>' in content
    assert '<input type="text" name="date" value="2000-01-01 03:02:01"' in content
    assert '<input type="number" name="distance" value="10.0"' in content
    assert '<input type="text" name="time" value="00:16:40"' in content
    assert '<input type="number" name="temperature" value="10.0"' in content
    assert '<input type="number" name="ascent" value="100.0"' in content
    assert '<input type="number" name="descent" value="0.0"' in content
    assert '<input type="number" name="max_speed" value="15.0"' in content
    assert '<input type="number" name="heart_rate" value="140"' in content
    assert '<input type="number" name="cadence" value="85"' in content


def test_data_update(client_logged):
    obj = DataFactory()
    data = {
        "bike": str(obj.bike.id),
        "date": date(2000, 1, 1),
        "distance": 10.12,
        "time": timedelta(seconds=15),
        "temperature": 1.1,
        "ascent": 600,
        "descent": 500,
        "max_speed": 110,
        "cadence": 120,
        "heart_rate": 200,
    }

    url = reverse("data:data_update", kwargs={"pk": obj.pk})
    client_logged.post(url, data=data, follow=True)

    actual = Data.objects.get(pk=obj.pk)

    assert actual.date == datetime(2000, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    assert actual.distance == 10.12
    assert actual.time == timedelta(seconds=15)
    assert actual.temperature == 1.1
    assert actual.ascent == 600
    assert actual.descent == 500
    assert actual.max_speed == 110
    assert actual.cadence == 120
    assert actual.heart_rate == 200


def test_data_update_bike(client_logged):
    bike = BikeFactory(short_name="xxx")
    obj = DataFactory()

    data = {
        "bike": str(bike.id),
        "date": obj.date,
        "distance": obj.distance,
        "time": obj.time,
        "temperature": obj.temperature,
        "ascent": obj.ascent,
        "descent": obj.descent,
        "max_speed": obj.max_speed,
        "cadence": obj.cadence,
        "heart_rate": obj.heart_rate,
    }

    url = reverse("data:data_update", kwargs={"pk": obj.pk})
    client_logged.post(url, data=data)
    actual = Data.objects.first()

    assert actual.bike == bike
    assert actual.date == datetime(2000, 1, 1, 3, 2, 1, tzinfo=timezone.utc)
    assert actual.distance == 10.0
    assert actual.time == timedelta(seconds=1000)
    assert actual.temperature == 10.0
    assert actual.ascent == 100
    assert actual.descent == 0
    assert actual.max_speed == 15
    assert actual.cadence == 85
    assert actual.heart_rate == 140


def test_bike_quick_update_func():
    view = resolve("/data/quick_update/1/")

    assert views.QuickUpdate is view.func.view_class


def test_data_quick_update_not_loged(client):
    data = DataFactory()
    url = reverse("data:data_quick_update", kwargs={"pk": data.pk})
    response = client.get(url, follow=True)
    assert response.resolver_match.func.view_class is Login


def test_data_quick_update_404(client_logged):
    url = reverse("data:data_quick_update", kwargs={"pk": 99})
    response = client_logged.get(url)

    assert response.status_code == 404


def test_data_quick_update_200(client_logged):
    data = DataFactory()
    url = reverse("data:data_quick_update", kwargs={"pk": data.pk})
    response = client_logged.get(url)

    assert response.status_code == 200


def test_data_quick_update(client_logged):
    obj = DataFactory()

    assert obj.checked == "n"

    url = reverse("data:data_quick_update", kwargs={"pk": obj.pk})

    client_logged.get(url)

    actual = Data.objects.get(pk=obj.pk)
    assert actual.checked == "y"
