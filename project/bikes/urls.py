from django.urls import path

from . import views

app_name = 'bikes'

urlpatterns = [
    path('component/', views.component_lists, name='component_list'),
    path('component/create/', views.component_create, name='component_create'),
    path('component/update/<int:pk>/', views.component_update, name='component_update'),
    path('component/delete/<int:pk>/', views.component_delete, name='component_delete'),

    path('<slug:bike_slug>/component/', views.ComponentWearIndex.as_view(), name='stats_index'),
    path('<slug:bike_slug>/component/<int:component_pk>/detail/', views.ComponentWearDetail.as_view(), name='stats_detail'),
    path('<slug:bike_slug>/component/<int:component_pk>/', views.ComponentWearList.as_view(), name='stats_list'),
    path('<slug:bike_slug>/component/<int:component_pk>/create/', views.bike_stats_create, name='stats_create'),
    path('<slug:bike_slug>/component/<int:stats_pk>/update/', views.bike_stats_update, name='stats_update'),
    path('<slug:bike_slug>/component/<int:stats_pk>/delete/', views.bike_stats_delete, name='stats_delete'),

    path('bike/', views.bike_lists, name='bike_list'),
    path('bike/create/', views.bike_create, name='bike_create'),
    path('bike/update/<int:pk>/', views.bike_update, name='bike_update'),
    path('bike/delete/<int:pk>/', views.bike_delete, name='bike_delete'),

    path('info/', views.bike_info_index, name='info_index'),
    path('<slug:bike_slug>/info/', views.bike_info_lists, name='info_list'),
    path('<slug:bike_slug>/info/create/', views.bike_info_create, name='info_create'),
    path('<slug:bike_slug>/info/update/<int:pk>/', views.bike_info_update, name='info_update'),
    path('<slug:bike_slug>/info/delete/<int:pk>/', views.bike_info_delete, name='info_delete'),
]
