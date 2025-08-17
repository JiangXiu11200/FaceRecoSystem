import os
import uuid
from datetime import datetime

from accounts.filters import AccountsFilter, AccountsGroupFilter
from accounts.models import SystemApps, UserGroup, UserProfile
from accounts.serializers.account import (
    AccountsPhotoStickersSerializer,
    AccountsSerializer,
    ChangePasswordSerializer,
    SystemAppsSerializer,
    UserGroupSerializer,
    UserRegisterSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
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
from utils.minio_client import MinioClient


class AccountsViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = AccountsSerializer
    filterset_fields = ["account"]
    filterset_class = AccountsFilter
    filter_backends = [DjangoFilterBackend]
    activity_logs = {
        "GET": "Search system accounts.",
        "PUT": "Update system account.",
        "DELETE": "Delete system account.",
    }

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.id == 1:
            return Response({"error": "Cannot delete default admin account."}, status=status.HTTP_400_BAD_REQUEST)
        MinioClient.delete_directory(bucket_name="accounts", directory_name=instance.account)

        return super().destroy(request, *args, **kwargs)


class AccountsPhotoStickersViewSet(CreateModelMixin, GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = AccountsPhotoStickersSerializer
    activity_logs = {"POST": "Upload photo stickers for user."}

    def create(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        uploaded_file = request.FILES.get("file")

        if not user_id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        if not uploaded_file:
            return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        validation_result = self.validate_image(uploaded_file)
        if not validation_result["valid"]:
            return Response({"error": validation_result["error"]}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_400_BAD_REQUEST)

        file_extension = self.get_file_extension(uploaded_file.name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        object_name = f"{user.account}/profile_picture_{timestamp}_{unique_id}{file_extension}"

        try:
            status_upload, result = self.upload_to_minio(uploaded_file, object_name)
            if not status_upload:
                return Response(
                    {"error": f"Failed to upload to storage: {result.get('error')}"},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

            status_get_url, image_url = self.get_minio_url(object_name)
            if not status_get_url:
                return Response(
                    {"error": f"Failed to get image URL: {image_url.get('error')}"},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

            if user.profile_picture_file_name:
                status_delete, delete_result = self.delete_minio_object(user.profile_picture_file_name)
                if not status_delete:
                    print(f"Failed to delete old photo stickers: {delete_result.get('error')}")

            user.profile_picture_file_name = object_name
            user.save()

            serializer = self.get_serializer(user)

            return Response(
                {
                    "user": serializer.data,
                    "image_url": image_url.get("url"),
                    "object_name": object_name,
                    "message": "Image uploaded successfully",
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            print(f"Error during file upload: {str(e)}")
            return Response({"error": f"Upload failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def validate_image(self, uploaded_file: bytes) -> dict:
        """驗證上傳的圖片"""
        max_size = 5 * 1024 * 1024
        if uploaded_file.size > max_size:
            return {"valid": False, "error": "File size must be less than 5MB"}

        allowed_types = ["image/jpeg", "image/jpg", "image/png"]
        if uploaded_file.content_type not in allowed_types:
            return {"valid": False, "error": f"Invalid file type: {uploaded_file.content_type}"}

        allowed_extensions = [".jpg", ".jpeg", ".png"]
        file_extension = self.get_file_extension(uploaded_file.name).lower()
        if file_extension not in allowed_extensions:
            return {"valid": False, "error": f"Invalid file extension: {file_extension}"}

        return {"valid": True}

    def get_file_extension(self, filename: str) -> str:
        return os.path.splitext(filename)[1]

    def upload_to_minio(self, uploaded_file: bytes, object_name: str) -> tuple[bool, dict]:
        file_content = uploaded_file.read()
        try:
            status_upload, result = MinioClient.upload_object(
                bucket_name="accounts",
                saved_object_name=object_name,
                absolute_path_or_binary=file_content,
                is_binary=True,
            )
            return status_upload, result
        except Exception as e:
            print(f"Error uploading to MinIO: {str(e)}")
            return False, {"status": False, "error": str(e)}

    def get_minio_url(self, object_name: str) -> str:
        try:
            status, result = MinioClient.get_object_url(
                bucket_name="accounts",
                object_name=object_name,
                expires_in_sec=3600,
            )
            return status, result
        except Exception as e:
            print(f"Error uploading to MinIO: {str(e)}")
            return False, {"status": False, "error": str(e)}

    def delete_minio_object(self, object_name: str) -> bool:
        try:
            status, result = MinioClient.delete_object(
                bucket_name="accounts",
                object_name=object_name,
            )
            return status, result
        except Exception as e:
            print(f"Error deleting object from MinIO: {str(e)}")
            return False, {"status": False, "error": str(e)}


class GroupViewSet(viewsets.ModelViewSet):
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupSerializer
    activity_logs = {
        "POST": "Create user group.",
        "PUT": "Update user group.",
        "DELETE": "Delete user group.",
    }
    filterset_fields = ["group_name"]
    filterset_class = AccountsGroupFilter
    filter_backends = [DjangoFilterBackend]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.id == 1:
            return Response({"error": "Cannot delete default user group."}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)


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
