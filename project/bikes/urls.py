from django.urls import path

from . import views
from .apps import App_name


app_name = App_name

urlpatterns = [
    # ......................................................................... Component
    path("component/", views.ComponentList.as_view(), name="component_list"),
    path("component/create/", views.ComponentCreate.as_view(), name="component_create"),
    path(
        "component/detail/<int:pk>/",
        views.ComponentDetail.as_view(),
        name="component_detail",
    ),
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
    # ............................................................... Component Statistic
    path("stats/<slug:bike_slug>/", views.StatsIndex.as_view(), name="stats_index"),
    path(
        "stats/<slug:bike_slug>/<int:component_pk>/",
        views.StatsList.as_view(),
        name="stats_list",
    ),
    path(
        "stats/<slug:bike_slug>/<int:component_pk>/create/",
        views.StatsCreate.as_view(),
        name="stats_create",
    ),
    path(
        "stats/<slug:bike_slug>/detail/<int:stats_pk>/",
        views.StatsDetail.as_view(),
        name="stats_detail",
    ),
    path(
        "stats/<slug:bike_slug>/update/<int:stats_pk>/",
        views.StatsUpdate.as_view(),
        name="stats_update",
    ),
    path(
        "stats/<slug:bike_slug>/delete/<int:stats_pk>/",
        views.StatsDelete.as_view(),
        name="stats_delete",
    ),
    # .............................................................................. Bike
    path("bike/", views.BikeList.as_view(), name="bike_list"),
    path("bike/create/", views.BikeCreate.as_view(), name="bike_create"),
    path("bike/detail/<int:pk>/", views.BikeDetail.as_view(), name="bike_detail"),
    path("bike/update/<int:pk>/", views.BikeUpdate.as_view(), name="bike_update"),
    path("bike/delete/<int:pk>/", views.BikeDelete.as_view(), name="bike_delete"),
    # ......................................................................... Bike Info
    path("info/", views.BikeInfoIndex.as_view(), name="info_index"),
    path("info/<slug:bike_slug>/", views.bike_info_lists, name="info_list"),
    path("info/<slug:bike_slug>/create/", views.bike_info_create, name="info_create"),
    path(
        "info/<slug:bike_slug>/update/<int:pk>/",
        views.bike_info_update,
        name="info_update",
    ),
    path(
        "info/<slug:bike_slug>/delete/<int:pk>/",
        views.bike_info_delete,
        name="info_delete",
    ),
]
