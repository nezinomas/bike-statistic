from django.urls import path

from .views import component, stats, bike, info

app_name = 'bikes'

urlpatterns = [
    path('component/', component.lists, name='component_list'),
    path('component/create/', component.create, name='component_create'),
    path('component/update/<int:pk>/', component.update, name='component_update'),
    path('component/delete/<int:pk>/', component.delete, name='component_delete'),

    path('component/<slug:bike_slug>/', stats.index, name='stats_index'),
    path('component/<slug:bike_slug>/<int:component_pk>', stats.lists, name='stats_list'),
    path('component/<slug:bike_slug>/<int:component_pk>/create', stats.create, name='stats_create'),
    path('component/<slug:bike_slug>/<int:stats_pk>/update', stats.update, name='stats_update'),
    path('component/<slug:bike_slug>/<int:stats_pk>/delete', stats.delete, name='stats_delete'),

    path('bike/', bike.lists, name='bike_list'),
    path('bike/create/', bike.create, name='bike_create'),
    path('bike/update/<int:pk>/', bike.update, name='bike_update'),
    path('bike/delete/<int:pk>/', bike.delete, name='bike_delete'),

    path('info/', info.index, name='info_index'),
    path('info/<slug:bike_slug>/', info.lists, name='info_list'),
    path('info/<slug:bike_slug>/create/', info.create, name='info_create'),
    path('info/<slug:bike_slug>/update/<int:pk>/', info.update, name='info_update'),
    path('info/<slug:bike_slug>/delete/<int:pk>', info.delete, name='info_delete'),
]
