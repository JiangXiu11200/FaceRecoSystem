from typing import Union

from accounts.models import UserProfile
from accounts.utils.jwt_utils import verify_access_jwt
from rest_framework import authentication, exceptions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request) -> Union[tuple, None]:
        """Authenticate the user using JWT token."""
        authorization = request.headers.get("Authorization")
        if not authorization or not authorization.startswith("Bearer "):
            return None

        token = authorization.split(" ")[1]
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
        if not user or not user.is_authenticated:
            raise AuthenticationFailed("Unauthorized.")

        jwt_token = request.headers.get("AUTHORIZATION")
        if jwt_token is None:
            raise AuthenticationFailed("Authorization header is missing.")

        user_group = getattr(user, "user_group", None)
        if user_group is None:
            raise AuthenticationFailed("Access denied.")

        allowed_app_names = list(user_group.apps.values_list("app_name", flat=True))
        path_segments = request.path.strip("/").split("/")
        api_prefix = path_segments[0] if path_segments else ""

        if api_prefix != "api":
            raise AuthenticationFailed("URL prefix.")

        allowed_app_names.extend(["token", "auth"])
        api_app_name = path_segments[1]
        if api_app_name not in allowed_app_names:
            raise AuthenticationFailed("Access denied.")

        return True
