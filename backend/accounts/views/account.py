from accounts.models import UserProfile
from accounts.serializers.account import ChangePasswordSerializer, UserRegisterSerializer
from rest_framework import status, viewsets
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class RegisterViewSet(CreateModelMixin, GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserRegisterSerializer


class ChangePasswordViewSet(viewsets.ViewSet):
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
