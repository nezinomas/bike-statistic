from django.urls import path, register_converter

from ..core import converters
from . import views
from .apps import App_name

app_name = App_name

register_converter(converters.DateConverter, 'date')

urlpatterns = [
    path('insert/', views.DataInsert.as_view(), name='data_insert'),
    path('list/', views.DataList.as_view(), name='data_list'),
    path('create/', views.DataCreate.as_view(), name='data_create'),
    path('update/<int:pk>/', views.DataUpdate.as_view(), name='data_update'),
    path('quick_update/<int:pk>/', views.QuickUpdate.as_view(), name='data_quick_update'),
    path('delete/<int:pk>/', views.DataDelete.as_view(), name='data_delete'),
]
