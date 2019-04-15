from django.urls import path, register_converter

from ..core import converters
from .views import chart, data

app_name = 'reports'

register_converter(converters.DateConverter, 'date')

urlpatterns = [
    path('', data.index, name='index'),
    path('data/', data.data_empty, name='data_empty'),
    path('data/insert/', data.insert_data, name='insert_data'),
    path(
        'data/<date:start_date>/',
        data.data_partial,
        name='data_partial'
    ),
    path(
        'data/<date:start_date>/<date:end_date>',
        data.data_list,
        name='data_list'
    ),
    path(
        'api/data/<date:start_date>/<date:end_date>/create/',
        data.data_create,
        name='data_create'
    ),
    path(
        'api/data/<date:start_date>/<date:end_date>/update/<int:pk>',
        data.data_update,
        name='data_update'
    ),
    path(
        'api/data/<date:start_date>/<date:end_date>/quick_update/<int:pk>',
        data.data_quick_update,
        name='data_quick_update'
    ),
    path(
        'api/data/<date:start_date>/<date:end_date>/delete/<int:pk>',
        data.data_delete,
        name='data_delete'
    ),

    path('api/reports/overall/', chart.api_overall, name='api-overall'),
    path('reports/overall/', chart.overall, name='overall'),
]
