from django.urls import path

from . import views

app_name = 'goals'

urlpatterns = [
    path('', views.GoalList.as_view(), name='goal_list'),
    path('create/', views.GoalCreate.as_view(), name='goal_create'),
    path('update/<int:pk>/', views.GoalUpdate.as_view(), name='goal_update'),
    path('delete/<int:pk>/', views.GoalDelete.as_view(), name='goal_delete'),
]
