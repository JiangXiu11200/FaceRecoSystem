from accounts.models import SystemApps, UserGroup, UserProfile
from accounts.serializers.account import (
    AccountsSerializer,
    ChangePasswordSerializer,
    SystemAppsSerializer,
    UserGroupSerializer,
    UserRegisterSerializer,
)
from rest_framework import status, viewsets
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class AccountsViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = AccountsSerializer
    activity_logs = {
        "GET": "Search system accounts.",
        "PUT": "Update system account.",
        "DELETE": "Delete system account.",
    }


class GroupViewSet(viewsets.ModelViewSet):
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupSerializer
    activity_logs = {
        "POST": "Create user group.",
        "PUT": "Update user group.",
        "DELETE": "Delete user group.",
    }


class RegisterViewSet(CreateModelMixin, GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserRegisterSerializer
    activity_logs = {"POST": "Register new user."}


class SystemAppsViewSet(ListModelMixin, GenericViewSet):
    queryset = SystemApps.objects.all()
    serializer_class = SystemAppsSerializer


class ChangePasswordViewSet(viewsets.ViewSet):
    activity_logs = {"POST": "Change user password."}

    def change_password(self, request, user_id):
        """Change password for a user."""
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request, "user": user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
