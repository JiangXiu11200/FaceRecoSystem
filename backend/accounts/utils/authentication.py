from typing import Union

from accounts.models import SystemApps, UserProfile
from accounts.utils.jwt_utils import verify_access_jwt
from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission

INTERNAL_TOKEN = settings.MICROSERVICE.get("internal_token", None)


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request) -> Union[tuple, None]:
        """Authenticate the user using JWT token."""
        internal_token = request.headers.get("X-Internal-Token", None)
        if internal_token == INTERNAL_TOKEN:
            user = "internal_service"
            return (user, None)

        token = request.headers.get("Authorization")
        if not token:
            raise AuthenticationFailed("Authorization header is missing.")
        payload = verify_access_jwt(token)

        if payload is None:
            raise exceptions.AuthenticationFailed("Invalid or expired token")

        try:
            user = UserProfile.objects.get(id=payload["user_id"])
        except UserProfile.DoesNotExist:
            raise exceptions.AuthenticationFailed("User not found")

        user.is_authenticated = True
        return (user, payload)


class Permission(BasePermission):
    def has_permission(self, request, view) -> bool:
        """User permission check."""
        user = request.user
        if user == "internal_service":
            return True

        if not user or not user.is_authenticated:
            raise AuthenticationFailed("Unauthorized.")

        jwt_token = request.headers.get("AUTHORIZATION")
        if jwt_token is None:
            raise AuthenticationFailed("Authorization header is missing.")

        allowed_app_names = list(SystemApps.objects.filter(user_groups__users=user).values_list("app_name", flat=True))
        if allowed_app_names is None or len(allowed_app_names) == 0:
            raise AuthenticationFailed("No app permissions.")

        path_segments = request.path.strip("/").split("/")
        api_prefix = path_segments[0] if path_segments else ""

        if api_prefix != "api":
            raise AuthenticationFailed("URL prefix.")

        allowed_app_names.extend(["token", "auth"])
        api_app_name = path_segments[1]
        if api_app_name not in allowed_app_names:
            raise AuthenticationFailed("Access denied.")

        return True
