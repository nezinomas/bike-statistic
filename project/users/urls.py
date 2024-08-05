from django.urls import path

from . import views

app_name = 'users'


urlpatterns = [
    path(
        'logout/',
        views.Logout.as_view(),
        name='logout'
    ),
    path(
        'login/',
        views.Login.as_view(template_name='users/login.html'),
        name='login'
    ),
    path('profile/sync/', views.sync_update, name='sync_update'),
]
