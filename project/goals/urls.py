from django.conf import settings
from django.conf.urls import static
from django.urls import path

from . import views

app_name = 'goals'

urlpatterns = [
    path('goals/', views.goals_list, name='goals_list'),
    path('api/goals/create/', views.goals_create, name='goals_create'),
    path('api/goals/update/<int:year>/', views.goals_update, name='goals_update'),
    path('api/goals/delete/<int:year>/', views.goals_delete, name='goals_delete'),
]
