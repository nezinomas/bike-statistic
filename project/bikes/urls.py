from django.urls import path

from .views import component, stats, bike, info

app_name = 'bikes'

urlpatterns = [
    path('component/', component.lists, name='component_list'),
    path('component/create/', component.create, name='component_create'),
    path('component/update/<int:pk>/', component.update, name='component_update'),
    path('component/delete/<int:pk>/', component.delete, name='component_delete'),

    path('<slug:bike_slug>/component/', stats.index, name='stats_index'),
    path('<slug:bike_slug>/component/<int:component_pk>/', stats.lists, name='stats_list'),
    path('<slug:bike_slug>/component/<int:component_pk>/create/', stats.create, name='stats_create'),
    path('<slug:bike_slug>/component/<int:stats_pk>/update/', stats.update, name='stats_update'),
    path('<slug:bike_slug>/component/<int:stats_pk>/delete/', stats.delete, name='stats_delete'),

    path('bike/', bike.lists, name='bike_list'),
    path('bike/create/', bike.create, name='bike_create'),
    path('bike/update/<int:pk>/', bike.update, name='bike_update'),
    path('bike/delete/<int:pk>/', bike.delete, name='bike_delete'),

    path('info/', info.index, name='info_index'),
    path('<slug:bike_slug>/info/', info.lists, name='info_list'),
    path('<slug:bike_slug>/info/create/', info.create, name='info_create'),
    path('<slug:bike_slug>/info/update/<int:pk>/', info.update, name='info_update'),
    path('<slug:bike_slug>/info/delete/<int:pk>/', info.delete, name='info_delete'),
]
