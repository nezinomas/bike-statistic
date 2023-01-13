from django.urls import path, register_converter

from ..core import converters
from . import views

app_name = 'reports'

register_converter(converters.DateConverter, 'date')

urlpatterns = [
    path('', views.DataList.as_view(), name='index'),
    path('data/insert/', views.insert_data, name='insert_data'),
    path('data/create/', views.DataCreate.as_view(), name='data_create'),
    path(
        'api/data/<date:start_date>/<date:end_date>/update/<int:pk>/',
        views.data_update,
        name='data_update'
    ),
    path('data/quick_update/<int:pk>/', views.QuickUpdate.as_view(), name='data_quick_update'),
    path('data/delete/<int:pk>/', views.DataDelete.as_view(), name='data_delete'),
    path('reports/overall/', views.overall, name='overall'),
    path('reports/<int:year>/', views.YearProgress.as_view(), name='year_progress'),
]
