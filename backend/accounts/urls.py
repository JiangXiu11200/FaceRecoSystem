from django.urls import include, path
from rest_framework import routers

from .views.account import (
    AccountsAvatarViewSet,
    AccountsProfilePictureViewSet,
    AccountsViewSet,
    ChangePasswordViewSet,
    GroupViewSet,
    RegisterViewSet,
    SystemAppsViewSet,
)
from .views.auth import LoginViewSet, LogoutViewSet, RefreshTokenViewSet

auth_router = routers.SimpleRouter()
auth_router.register(r"api/auth/login", LoginViewSet, basename="login")
auth_router.register(r"api/auth/logout", LogoutViewSet, basename="logout")
auth_router.register(r"api/token/refresh", RefreshTokenViewSet, basename="refresh-token")
accounts_router = routers.SimpleRouter()
accounts_router.register(r"api/accounts/register", RegisterViewSet, basename="accounts-register")
accounts_router.register(r"api/accounts/group", GroupViewSet, basename="accounts-group")
accounts_router.register(r"api/accounts/systemapps", SystemAppsViewSet, basename="accounts-systemapps")
accounts_router.register(
    r"api/accounts/upload-profile-picture", AccountsProfilePictureViewSet, basename="accounts-photo-stickers"
)
accounts_router.register(r"api/accounts/avatars", AccountsAvatarViewSet, basename="accounts-avatars")
accounts_router.register(r"api/accounts", AccountsViewSet, basename="accounts")


urlpatterns = [
    path(
        "api/accounts/change-password/<int:user_id>/",
        ChangePasswordViewSet.as_view({"post": "change_password"}),
        name="accounts-change-password",
    ),
    path(r"", include(auth_router.urls)),
    path(r"", include(accounts_router.urls)),
]
