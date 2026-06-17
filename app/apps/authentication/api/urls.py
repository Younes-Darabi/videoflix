from django.urls import path

from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    CustomTokenRefreshView,
    ActivateAccountView,
    PasswordResetView,
    PasswordResetConfirmView,
)


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "activate/<str:uidb64>/<str:token>/",
        ActivateAccountView.as_view(),
        name="activate",
    ),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("password_reset/", PasswordResetView.as_view(), name="password_reset"),
    path(
        "password_confirm/<str:uidb64>/<str:token>/",
        PasswordResetConfirmView.as_view(),
        name="password_confirm",
    ),
]
