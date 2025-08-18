import os
import uuid
from datetime import datetime

from accounts.filters import AccountsFilter, AccountsGroupFilter
from accounts.models import SystemApps, UserGroup, UserProfile
from accounts.serializers.account import (
    AccountsProfilePictureSerializer,
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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        object_names = [obj.profile_picture_file_name for obj in (page or queryset) if obj.profile_picture_file_name]

        urls = {}
        if object_names:
            try:
                state, results = MinioClient.get_multiple_objects_url(
                    bucket_name="accounts",
                    object_names=object_names,
                    expires_in_sec=3600,
                )
                urls = results.get("urls", {}) if state else {}
            except Exception:
                urls = {}

        serializer = self.get_serializer(page or queryset, many=True, context={"request": request, "minio_urls": urls})
        if page is not None:
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        profile_picture_file_name = request.data.get("profile_picture_file_name") or None
        delete_picture = request.data.get("delete_profile_picture", False)
        if profile_picture_file_name:
            move_status, move_result = MinioClient.move_to_new_bucket(
                source_bucket="temporary-data",
                destination_bucket="accounts",
                object_name=profile_picture_file_name,
                new_prefix=instance.account,
            )
            if move_status:
                profile_picture_file_name = move_result.get("new_object_name") if move_status else None
                instance.profile_picture_file_name = profile_picture_file_name if move_status else None
        if delete_picture:
            if instance.profile_picture_file_name:
                delete_status, delete_result = MinioClient.delete_object(
                    bucket_name="accounts",
                    object_name=instance.profile_picture_file_name,
                )
                if delete_status:
                    instance.profile_picture_file_name = None

        instance.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.id == 1:
            return Response({"error": "Cannot delete default admin account."}, status=status.HTTP_400_BAD_REQUEST)
        MinioClient.delete_directory(bucket_name="accounts", directory_name=instance.account)

        return super().destroy(request, *args, **kwargs)

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


class AccountsProfilePictureViewSet(CreateModelMixin, GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = AccountsProfilePictureSerializer
    activity_logs = {"POST": "Upload photo stickers for user."}

    def create(self, request):
        uploaded_file = request.FILES.get("file")

        if not uploaded_file:
            return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        validation_result = self.validate_image(uploaded_file)
        if not validation_result["valid"]:
            return Response({"error": validation_result["error"]}, status=status.HTTP_400_BAD_REQUEST)

        file_extension = self.get_file_extension(uploaded_file.name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        file_name = f"accounts/profile_picture_{timestamp}_{unique_id}{file_extension}"

        try:
            status_upload, result = self.upload_to_minio(uploaded_file, file_name)
            if not status_upload:
                return Response(
                    {"error": f"Failed to upload to storage: {result.get('error')}"},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

            status_get_url, image_url = self.get_minio_url(file_name)
            if not status_get_url:
                return Response(
                    {"error": f"Failed to get image URL: {image_url.get('error')}"},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )
            return Response(
                {
                    "image_url": image_url.get("url"),
                    "file_name": file_name,
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
                bucket_name="temporary-data",
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
                bucket_name="temporary-data",
                object_name=object_name,
                expires_in_sec=3600,
            )
            return status, result
        except Exception as e:
            print(f"Error uploading to MinIO: {str(e)}")
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

    def create(self, request):
        """Create a new user account."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        profile_picture_file_name = request.data.get("profile_picture_file_name") or None
        if profile_picture_file_name:
            move_status, move_result = MinioClient.move_to_new_bucket(
                source_bucket="temporary-data",
                destination_bucket="accounts",
                object_name=profile_picture_file_name,
                new_prefix=user.account,
            )
            if move_status:
                profile_picture_file_name = move_result.get("new_object_name") if move_status else None
                user.profile_picture_file_name = profile_picture_file_name if move_status else None
        user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


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

class AccountsAvatarViewSet(GenericViewSet):
    def list(self, request, *args, **kwargs):
        profile_picture_file_name = request.query_params.get("profile_picture_file_name")
        if not profile_picture_file_name:
            return Response({"error": "Missing profile picture file name"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            status_get_url, results = MinioClient.get_object_url(
                bucket_name="accounts",
                object_name=profile_picture_file_name,
                expires_in_sec=1800,
            )
            if status_get_url:
                return Response({"url": results.get("url")}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Failed to get presigned URL"}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({"error": "MinIO connection failed"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
