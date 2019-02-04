from django.urls import path

from .views import component, stats

app_name = 'bikes'

urlpatterns = [
    path('component/', component.component_list, name='component_list'),
    path('component/create/', component.component_create, name='component_create'),
    path('component/update/<int:pk>/', component.component_update, name='component_update'),
    path('component/delete/<int:pk>/', component.component_delete, name='component_delete'),
    path('component/<slug:bike>/', stats.stats_list, name='stats_list'),
    path('component/<slug:bike>/<int:pk>/create', stats.stats_create, name='stats_create'),
    path('component/<slug:bike>/<int:pk>/update', stats.stats_update, name='stats_update'),
    path('component/<slug:bike>/<int:pk>/delete', stats.stats_delete, name='stats_delete'),
]
