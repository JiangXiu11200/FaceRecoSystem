from django.urls import include, path
from rest_framework import routers

from .views.account import RegisterViewSet
from .views.auth import LoginViewSet, LogoutViewSet, RefreshTokenViewSet

auth_router = routers.SimpleRouter()
auth_router.register(r"api/auth/login", LoginViewSet, basename="login")
auth_router.register(r"api/auth/logout", LogoutViewSet, basename="logout")
auth_router.register(r"api/token/refresh", RefreshTokenViewSet, basename="refresh-token")
accounts_router = routers.SimpleRouter()
auth_router.register(r"api/accounts/register", RegisterViewSet, basename="register")


urlpatterns = [
    path(r"", include(auth_router.urls)),
    path(r"", include(accounts_router.urls)),
]
