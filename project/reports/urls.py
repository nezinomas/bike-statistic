from django.urls import path, register_converter

from ..core import converters
from . import views
from .apps import App_name

app_name = App_name

register_converter(converters.DateConverter, 'date')

urlpatterns = [
    path('overall/', views.ChartOverall.as_view(), name='chart_overall'),
    path('extremums/', views.Extremums.as_view(), name='extremums'),
    path('<int:year>/', views.YearProgress.as_view(), name='year_progress'),
]
