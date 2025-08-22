import datetime

from accounts.models import UserProfile
from accounts.serializers.auth import LoginSerializer
from accounts.utils.jwt_utils import generate_access_jwt, generate_refresh_jwt, verify_refresh_jwt
from activity_logs.utils.create_system_activity import create_system_activity
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class LoginViewSet(CreateModelMixin, GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = LoginSerializer
    authentication_classes = []
    permission_classes = []
    activity_logs = {"POST": "Login."}

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": "Invalid username or password, please try again."}, status=status.HTTP_400_BAD_REQUEST
            )

        validated = serializer.validated_data
        user_id = validated["user_id"]
        account = validated["account"]
        permissions = validated["permissions"]
        is_active = validated["is_active"]
        group_active = validated["group_active"]
        keep_days = validated.get("keep_expiration_days", 1)  # Default refresh token expiration to 1 day
        profile_picture_file_name = validated.get("profile_picture_file_name")

        if not is_active:
            return Response({"message": "User account is inactive."}, status=status.HTTP_403_FORBIDDEN)
        if not group_active:
            return Response({"message": "User group is inactive."}, status=status.HTTP_403_FORBIDDEN)

        if len(permissions) == 0:
            return Response({"message": "No permissions found for this user."}, status=status.HTTP_403_FORBIDDEN)

        access_token, refresh_token = self.generate_tokens(user_id, account, permissions, keep_days)

        if not access_token or not refresh_token:
            return Response({"message": "Token generation failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = Response({"access_token": access_token}, status=status.HTTP_200_OK)

        if validated.get("remember_me"):
            self.set_refresh_cookie(response, refresh_token, keep_days)

        if profile_picture_file_name:
            response.data["profile_picture_file_name"] = profile_picture_file_name
        response.data["account"] = account
        response.data["user_id"] = user_id

        self.create_login_activity(user=account, status_code=status.HTTP_200_OK, activity="Login successful.")

        return response

    def generate_tokens(self, user_id: int, account: str, permissions: list, days: int) -> tuple:
        """Generate access and refresh tokens."""
        access_token = generate_access_jwt(user_id, account, permissions)
        refresh_token = generate_refresh_jwt(user_id, account, permissions, days)
        return access_token, refresh_token

    def set_refresh_cookie(self, response: Response, refresh_token: str, days: int) -> None:
        """Set the refresh token in a secure cookie."""
        expires = datetime.datetime.utcnow() + datetime.timedelta(days=days)
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,  # (settings.DEBUG is False),  # Use secure cookies in production
            samesite="Lax",
            expires=expires.strftime("%a, %d-%b-%Y %H:%M:%S GMT"),
        )

    def create_login_activity(
        self, user: str, status_code: int, activity: str, message: str = None, actions: str = "POST"
    ) -> bool:
        """
        Log a successful login activity.
        """
        return create_system_activity(user, actions, status_code, activity, message)


class LogoutViewSet(CreateModelMixin, GenericViewSet):
    queryset = []
    activity_logs = {"POST": "Logout."}
    authentication_classes = []
    permission_classes = []

    def create(self, request):
        """Handle user logout by clearing the refresh token cookie."""
        # TODO: 需要透過 Redis 或 DB 來管理 Refresh Token 的有效性，登出時應該將對應的 Refresh Token 刪除
        response = Response({"detail": "Logged out successfully"}, status=status.HTTP_200_OK)
        response.delete_cookie("refresh_token")
        return response


class RefreshTokenViewSet(CreateModelMixin, GenericViewSet):
    queryset = []
    activity_logs = {"POST": "Refresh Token."}
    authentication_classes = []
    permission_classes = []

    def create(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response({"detail": "Refresh token not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        payload = verify_refresh_jwt(refresh_token)
        if not payload:
            return Response({"detail": "Invalid or expired refresh token."}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = payload["user_id"]
        account = payload["account"]
        permissions = payload.get("permissions")

        access_token = generate_access_jwt(user_id, account, permissions)

        return Response({"access_token": access_token}, status=status.HTTP_200_OK)
