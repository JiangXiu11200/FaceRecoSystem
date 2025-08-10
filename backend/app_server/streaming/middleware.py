from urllib.parse import parse_qs

from accounts.models import UserProfile
from accounts.utils.jwt_utils import verify_access_jwt
from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from rest_framework import exceptions


@database_sync_to_async
def get_user_from_token(token):
    if not token:
        raise exceptions.AuthenticationFailed("No token provided")

    payload = verify_access_jwt(token)
    if not payload:
        raise exceptions.AuthenticationFailed("Invalid or expired token")

    try:
        user = UserProfile.objects.get(id=payload["user_id"])
        user.is_authenticated = True
        return user
    except UserProfile.DoesNotExist:
        raise exceptions.AuthenticationFailed("User not found")


class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        token = None
        try:
            query_string = scope.get("query_string", b"").decode()
            query_params = parse_qs(query_string)
            if "token" in query_params:
                token = query_params["token"][0]

            if not token:
                headers = dict(scope.get("headers", []))
                auth_header = headers.get(b"authorization", b"")
                token = auth_header.decode() if auth_header else None

            if settings.USE_AUTHENTICATION:
                user = await get_user_from_token(token)
                scope["user"] = user
            else:
                scope["user"] = AnonymousUser()

            return await self.inner(scope, receive, send)
        except exceptions.AuthenticationFailed:
            await send({"type": "websocket.close", "code": 4001})
            return
