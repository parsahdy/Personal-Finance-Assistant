from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views


urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/update/", views.ProfileUpdateView.as_view(), name="profile-update"),
    path("change-password/", views.ChangePasswordView.as_view(), name="change-password"),
]