from django.urls import path

from . import views

app_name = 'bikes'

urlpatterns = [
    path('component/', views.component_list, name='component_list'),
    path('component/create/', views.component_create, name='component_create'),
    path('component/update/<int:pk>/', views.component_update, name='component_update'),
    path('component/delete/<int:pk>/', views.component_delete, name='component_delete'),
    path('component/<slug:bike>/', views.stats_list, name='stats_list'),
    path('component/<slug:bike>/<int:pk>/create', views.stats_create, name='stats_create'),
    path('component/<slug:bike>/<int:pk>/update', views.stats_update, name='stats_update'),
    path('component/<slug:bike>/<int:pk>/deleta', views.stats_delete, name='stats_delete'),
]
