from django.urls import path

from . import views

app_name = 'goals'

urlpatterns = [
    path('', views.GoalsList.as_view(), name='goal_list'),
    path('create/', views.goals_create, name='goal_create'),
    path('update/<int:year>/', views.goals_update, name='goal_update'),
    path('delete/<int:year>/', views.goals_delete, name='goal_delete'),
]
