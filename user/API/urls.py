from django.urls import path

from user.API.views import UserListView, RegisterUserAPIView, LoginUserAPIView

urlpatterns = [
    path('user_view/', UserListView.as_view(), name='api_user_view'),
    path('register_view/', RegisterUserAPIView.as_view(), name='api_register_view'),
    path('login_view/', LoginUserAPIView.as_view(), name='api_login_view'),
]