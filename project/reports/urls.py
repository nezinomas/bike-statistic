from django.conf import settings
from django.conf.urls import static
from django.urls import path
from django.views.i18n import JavaScriptCatalog

from . import views

app_name = 'reports'

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.ViewData.as_view(), name='index'),
    path('f/', views.test, name='index1'),
]
