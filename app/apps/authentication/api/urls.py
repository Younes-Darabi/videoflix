from django.urls import path

from .views import RegisterView, LogoutView, LoginView, TokenRefreshView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='Login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]