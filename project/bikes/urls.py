from django.urls import path

from . import views
from .apps import App_name

app_name = App_name

urlpatterns = [
    # ........................................................................Component
    path("component/", views.ComponentList.as_view(), name="component_list"),
    path("component/create/", views.ComponentCreate.as_view(), name="component_create"),
    path(
        "component/update/<int:pk>/",
        views.ComponentUpdate.as_view(),
        name="component_update",
    ),
    path(
        "component/delete/<int:pk>/",
        views.ComponentDelete.as_view(),
        name="component_delete",
    ),
    # ...................................................   .............Component Wear
    path(
        "wear/<slug:bike_slug>/",
        views.ComponentWearList.as_view(),
        name="wear_list",
    ),
    path(
        "wear/<slug:bike_slug>/<int:component_pk>/",
        views.ComponentWearList.as_view(),
        name="wear_list",
    ),
    path(
        "wear/<slug:bike_slug>/<int:component_pk>/create/",
        views.ComponentWearCreate.as_view(),
        name="wear_create",
    ),
    path(
        "wear/<slug:bike_slug>/update/<int:wear_pk>/",
        views.ComponentWearUpdate.as_view(),
        name="wear_update",
    ),
    path(
        "wear/<slug:bike_slug>/delete/<int:wear_pk>/",
        views.ComponentWearDelete.as_view(),
        name="wear_delete",
    ),
    # .............................................................................Bike
    path("bike/", views.BikeList.as_view(), name="bike_list"),
    path("bike/create/", views.BikeCreate.as_view(), name="bike_create"),
    path("bike/update/<int:pk>/", views.BikeUpdate.as_view(), name="bike_update"),
    path("bike/delete/<int:pk>/", views.BikeDelete.as_view(), name="bike_delete"),
    # ........................................................................Bike Info
    path("info/<slug:bike_slug>/", views.BikeInfoList.as_view(), name="info_list"),
    path(
        "info/<slug:bike_slug>/create/",
        views.BikeInfoCreate.as_view(),
        name="info_create",
    ),
    path(
        "info/<slug:bike_slug>/update/<int:pk>/",
        views.BikeInfoUpdate.as_view(),
        name="info_update",
    ),
    path(
        "info/<slug:bike_slug>/delete/<int:pk>/",
        views.BikeInfoDelete.as_view(),
        name="info_delete",
    ),
]
