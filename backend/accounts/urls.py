from django.urls import include, path
from rest_framework import routers

from .views import LoginViewSet, LogoutViewSet, RefreshTokenViewSet, RegisterViewSet

router = routers.SimpleRouter()
router.register(r"api/auth/login", LoginViewSet, basename="login")
router.register(r"api/auth/logout", LogoutViewSet, basename="logout")
router.register(r"api/auth/register", RegisterViewSet, basename="register")
router.register(r"api/token/refresh", RefreshTokenViewSet, basename="refresh-token")
# router.register(r"api/auth/change-password/{id}", RegisterViewSet, basename="user")

urlpatterns = [
    path(r"", include(router.urls)),
]
