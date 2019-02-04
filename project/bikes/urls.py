from django.urls import path

from .views import component, stats

app_name = 'bikes'

urlpatterns = [
    path('component/', component.lists, name='component_list'),
    path('component/create/', component.create, name='component_create'),
    path('component/update/<int:pk>/', component.update, name='component_update'),
    path('component/delete/<int:pk>/', component.delete, name='component_delete'),
    path('component/<slug:bike>/', stats.lists, name='stats_list'),
    path('component/<slug:bike>/<int:pk>/create', stats.create, name='stats_create'),
    path('component/<slug:bike>/<int:pk>/update', stats.update, name='stats_update'),
    path('component/<slug:bike>/<int:pk>/delete', stats.delete, name='stats_delete'),
]
