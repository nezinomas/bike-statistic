from django.urls import path, register_converter

from ..core import converters

from . import views

app_name = 'reports'

register_converter(converters.DateConverter, 'date')

urlpatterns = [
    path('', views.index, name='index'),
    path('data/', views.data_empty, name='data_empty'),
    path('data/insert/', views.insert_data, name='insert_data'),
    path(
        'data/<date:start_date>/',
        views.data_partial,
        name='data_partial'
    ),
    path(
        'data/<date:start_date>/<date:end_date>',
        views.data_list,
        name='data_list'
    ),
    path(
        'api/data/<date:start_date>/<date:end_date>/create/',
        views.data_create,
        name='data_create'
    ),
    path(
        'api/data/<date:start_date>/<date:end_date>/update/<int:pk>',
        views.data_update,
        name='data_update'
    ),
    path(
        'api/data/<date:start_date>/<date:end_date>/quick_update/<int:pk>',
        views.data_quick_update,
        name='data_quick_update'
    ),
    path(
        'api/data/<date:start_date>/<date:end_date>/delete/<int:pk>',
        views.data_delete,
        name='data_delete'
    ),

    path('api/reports/overall/', views.api_overall, name='api-overall'),
    path('reports/overall/', views.overall, name='overall'),
]
