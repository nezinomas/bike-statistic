from django.urls import path

from . import views

app_name = 'goals'

urlpatterns = [
    path('', views.GoalsList.as_view(), name='goal_list'),
    path('create/', views.goals_create, name='goal_create'),
    path('detail/<int:pk>/', views.GoalDetail.as_view(), name='goal_detail'),
    path('update/<int:pk>/', views.goals_update, name='goal_update'),
    path('delete/<int:pk>/', views.goals_delete, name='goal_delete'),
]
