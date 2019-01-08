from django.urls import path

from . import views

app_name = 'bikes'

urlpatterns = [
    path('component/', views.component_list, name='component_list'),
    path('component/create/', views.component_create, name='component_create'),
    path('component/update/<int:pk>/', views.component_update, name='component_update'),
    path('component/delete/<int:pk>/', views.component_delete, name='component_delete'),
]
