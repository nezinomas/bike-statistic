from django.urls import path, register_converter

from ..core import converters

from . import views

app_name = 'reports'

register_converter(converters.DateConverter, 'date')

urlpatterns = [
    # path('', views.index, name='index'),
    path('f/', views.test, name='index1'),
    path('data/', views.data_table_empty_date, name='data_table_empty_date'),
    path('data/<date:start_date>/', views.data_table_no_end, name='data_table_no_end'),
    path('data/<date:start_date>/<date:end_date>', views.data_table, name='data_table'),
    path('data/get', views.get_data, name='get_data'),
]
