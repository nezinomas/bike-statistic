from django.urls import path, register_converter

from ..core import converters

from . import views

app_name = 'reports'

register_converter(converters.DateConverter, 'date')

urlpatterns = [
    path('data/', views.data_table_empty_date, name='data_table_empty_date'),
    path('data/<date:start_date>/', views.data_table_no_end, name='data_table_no_end'),
    path('data/<date:start_date>/<date:end_date>/', views.data_table, name='data_table'),
    path('data/insert/', views.insert_data, name='insert_data'),
    path('api/reports/overall/', views.api_overall, name='api-overall'),
    path('reports/overall/', views.overall, name='overall'),

    path('data1/', views.data_empty, name='data_empty'),
    path('data1/<date:start_date>/', views.data_partial, name='data_partial'),
    path('data1/<date:start_date>/<date:end_date>', views.data_list, name='data_list'),
    path('api/data/<date:start_date>/<date:end_date>/create/', views.data_create, name='data_create'),
    path('api/data/<date:start_date>/<date:end_date>/update/<int:pk>', views.data_update, name='data_update'),
    path('api/data/<date:start_date>/<date:end_date>/delete/<int:pk>', views.data_delete, name='data_delete'),
]
