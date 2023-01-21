from django.urls import path

from . import views
from .apps import App_name


app_name = App_name

urlpatterns = [
    path('component/', views.component_lists, name='component_list'),
    path('component/create/', views.component_create, name='component_create'),
    path('component/update/<int:pk>/', views.component_update, name='component_update'),
    path('component/delete/<int:pk>/', views.component_delete, name='component_delete'),

    path('stats/<slug:bike_slug>/', views.StatsIndex.as_view(), name='stats_index'),
    path('stats/<slug:bike_slug>/<int:component_pk>/', views.StatsList.as_view(), name='stats_list'),
    path('stats/<slug:bike_slug>/<int:component_pk>/create/', views.StatsCreate.as_view(), name='stats_create'),
    path('stats/<slug:bike_slug>/detail/<int:stats_pk>/', views.StatsDetail.as_view(), name='stats_detail'),
    path('stats/<slug:bike_slug>/update/<int:stats_pk>/', views.StatsUpdate.as_view(), name='stats_update'),
    path('stats/<slug:bike_slug>/delete/<int:stats_pk>/', views.StatsDelete.as_view(), name='stats_delete'),

    path('bike/', views.BikeList.as_view(), name='bike_list'),
    path('bike/create/', views.BikeCreate.as_view(), name='bike_create'),
    path('bike/detail/<int:pk>/', views.BikeDetail.as_view(), name='bike_detail'),
    path('bike/update/<int:pk>/', views.BikeUpdate.as_view(), name='bike_update'),
    path('bike/delete/<int:pk>/', views.bike_delete, name='bike_delete'),

    path('info/', views.bike_info_index, name='info_index'),
    path('info/<slug:bike_slug>/', views.bike_info_lists, name='info_list'),
    path('info/<slug:bike_slug>/create/', views.bike_info_create, name='info_create'),
    path('info/<slug:bike_slug>/update/<int:pk>/', views.bike_info_update, name='info_update'),
    path('info/<slug:bike_slug>/delete/<int:pk>/', views.bike_info_delete, name='info_delete'),
]
