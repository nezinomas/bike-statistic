from django.urls import path, register_converter

from ..core import converters
from . import views
from .apps import App_name

app_name = App_name

register_converter(converters.DateConverter, 'date')

urlpatterns = [
    path('overall/', views.overall, name='overall'),
    path('<int:year>/', views.YearProgress.as_view(), name='year_progress'),
]
