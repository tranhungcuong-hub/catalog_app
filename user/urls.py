from django.urls import path

from user import views


urlpatterns = [
    path("registration/", views.register, name='register'),
    path("login/", views.SignIn, name='login'),
    path("home/", views.homepage, name='home'),
    path("logout/", views.Logout, name='logout'),
    path("profile/", views.profile, name='profile'),
    path("", views.homepage),
]