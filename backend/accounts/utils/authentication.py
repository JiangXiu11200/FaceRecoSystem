from typing import Union

from accounts.models import UserProfile
from accounts.utils.jwt_utils import verify_access_jwt
from rest_framework import authentication, exceptions


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

        return (user, payload)
