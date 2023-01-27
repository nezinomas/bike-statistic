from django.urls import path

from . import views

app_name = 'goals'

urlpatterns = [
    path('', views.GoalList.as_view(), name='goal_list'),
    path('create/', views.GoalCreate.as_view(), name='goal_create'),
    path('detail/<int:pk>/', views.GoalDetail.as_view(), name='goal_detail'),
    path('update/<int:pk>/', views.GoalUpdate.as_view(), name='goal_update'),
    path('delete/<int:pk>/', views.goals_delete, name='goal_delete'),
]
