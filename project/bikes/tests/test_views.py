import pytest
from django.urls import resolve, reverse

from ...bikes.factories import BikeFactory, ComponentFactory
from .. import views

pytestmark = pytest.mark.django_db


# ---------------------------------------------------------------------------------------
#                                                                               bike list
# ---------------------------------------------------------------------------------------
def test_bike_list_func():
    view = resolve('/bike/')

    assert views.bike.lists == view.func


def test_bike_list_200_no_data(client_logged):
    url = reverse('bikes:bike_list')
    response = client_logged.get(url)

    assert response.status_code == 200


def test_bike_list_200(client_logged):
    url = reverse('bikes:bike_list')
    response = client_logged.get(url)

    assert response.status_code == 200


def test_bike_list_no_records(client_logged):
    url = reverse('bikes:bike_list')
    response = client_logged.get(url)

    assert '<td class="bg-warning text-center" colspan="4">No records</td>' in str(
        response.content)


# ---------------------------------------------------------------------------------------
#                                                                              info index
# ---------------------------------------------------------------------------------------
def test_bike_info_index_func():
    view = resolve('/info/')

    assert views.info.index == view.func


def test_bike_info_index_302(client_logged):
    url = reverse('bikes:info_index')
    response = client_logged.get(url)

    assert response.status_code == 302


def test_bike_info_index_no_records(client_logged):
    url = reverse('bikes:info_index')
    response = client_logged.get(url, follow=True)

    assert '<td class="bg-warning text-center" colspan="3">No records</td>' in str(
        response.content)


# ---------------------------------------------------------------------------------------
#                                                                              info list
# ---------------------------------------------------------------------------------------
def test_bike_info_list_func():
    view = resolve('/xxx/info/')

    assert views.info.lists == view.func


def test_bike_info_list_200(client_logged):
    url = reverse('bikes:info_list', kwargs={'bike_slug': 'xxx'})
    response = client_logged.get(url)

    assert response.status_code == 200


def test_bike_info_list_no_records(client_logged):
    url = reverse('bikes:info_list', kwargs={'bike_slug': 'xxx'})
    response = client_logged.get(url)

    assert '<td class="bg-warning text-center" colspan="3">No records</td>' in str(
        response.content)


# ---------------------------------------------------------------------------------------
#                                                                         component index
# ---------------------------------------------------------------------------------------
def test_component_index_func():
    view = resolve('/xxx/component/')

    assert views.stats.index == view.func


def test_component_index_302(client_logged):
    url = reverse('bikes:stats_index', kwargs={'bike_slug': 'x'})
    response = client_logged.get(url)

    assert response.status_code == 302


def test_component_index_no_records(client_logged):
    url = reverse('bikes:stats_index', kwargs={'bike_slug': 'x'})
    response = client_logged.get(url, follow=True)

    assert response.status_code == 200
    assert response.resolver_match.view_name == 'bikes:component_list'


# ---------------------------------------------------------------------------------------
#                                                                component statistic list
# ---------------------------------------------------------------------------------------
def test_stats_list_func():
    view = resolve('/xxx/component/1/')

    assert views.stats.lists == view.func


def test_stats_list_no_bike_no_componant(client_logged):
    url = reverse('bikes:stats_list', kwargs={'component_pk': 0, 'bike_slug': 'x'})
    response = client_logged.get(url, follow=True)

    assert response.status_code == 200


def test_stats_list_200(client_logged):
    b = BikeFactory()
    c = ComponentFactory()

    url = reverse('bikes:stats_list', kwargs={'component_pk': c.pk, 'bike_slug': b.slug})
    response = client_logged.get(url)

    assert response.status_code == 200


def test_stats_list_no_records(client_logged):
    b = BikeFactory()
    c = ComponentFactory()

    url = reverse('bikes:stats_list',
                  kwargs={
                    'component_pk': c.pk,
                    'bike_slug': b.slug
                 })

    response = client_logged.get(url)

    assert '<td class="bg-warning text-center" colspan="6">No records</td>' in str(
        response.content)
