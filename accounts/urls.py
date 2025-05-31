from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = "accounts"
urlpatterns = [
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", views.TokenVerifyView.as_view(), name="token_verify"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("signup-google/", views.SignupGoogleView.as_view(), name="signup_google"),
    path("signin/", views.SigninView.as_view(), name="signin"),
    path("signin-google/", views.SigninGoogleView.as_view(), name="signin"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("info/", views.UserInfoView.as_view(), name="info"),
    path(
        "password-reset-mail/",
        views.PasswordResetMailView.as_view(),
        name="password_reset_mail",
    ),
    path(
        "otp-verify/",
        views.OTPVerifyView.as_view(),
        name="otp_verify",
    ),
    path(
        "password-reset/",
        views.PasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password-change/",
        views.PasswordChangeView.as_view(),
        name="password_change",
    ),
]
