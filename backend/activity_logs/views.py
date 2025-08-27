from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.response import Response
from utils.minio_client import MinioClient

from activity_logs.utils.celery_scheduler_control import update_cleanup_old_activity_logs_task

from .filters import FaceRecognitionActivityLogsFilter, SystemActivityLogsFilter
from .models import (
    FaceRecognitionActivityLogs,
    FaceRecognitionActivityLogsRetention,
    SystemActivityLogsRetention,
    SystemActivtiyLogs,
)
from .serializers import (
    FaceRecognitionActivityLogsRetentionSerializer,
    FaceRecognitionActivityLogsSerializer,
    SystemActivityLogsRetentionSerializer,
    SystemActivityLogsSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="List system activity logs",
        description="Retrieve a list of system activity logs with optional filtering by account.",
    ),
    create=extend_schema(
        summary="Create a new system activity log entry",
        description="Create a new system activity log entry with the provided details.",
    ),
    destroy=extend_schema(
        summary="Delete a system activity log entry",
        description="Delete a specific system activity log entry by its ID.",
    ),
)
class SystemActivityLogsViewSet(ListModelMixin, CreateModelMixin, DestroyModelMixin, viewsets.GenericViewSet):
    queryset = SystemActivtiyLogs.objects.all().order_by("-timestamp")
    serializer_class = SystemActivityLogsSerializer
    filterset_class = SystemActivityLogsFilter
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["account"]


@extend_schema_view(
    create=extend_schema(
        summary="Create a new system activity log entry",
        description="Create a new system activity log entry with the provided details.",
    ),
)
class FaceRecognitionActivityLogsViewSet(ListModelMixin, CreateModelMixin, viewsets.GenericViewSet):
    queryset = FaceRecognitionActivityLogs.objects.all().order_by("-timestamp")
    serializer_class = FaceRecognitionActivityLogsSerializer
    filterset_class = FaceRecognitionActivityLogsFilter
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "group"]

    @extend_schema(
        summary="List facial recognition activity logs and obtain MinIO S3 face image Presigned URLs",
        description="Retrieve a list of facial recognition activity logs along with their corresponding MinIO S3 face image Presigned URLs.",
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        object_names = [obj.s3_object_key for obj in (page or queryset) if obj.s3_object_key]
        urls = {}

        if object_names:
            try:
                state, results = MinioClient.get_multiple_objects_url(
                    bucket_name="face-activity-logs",
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


@extend_schema_view(
    list=extend_schema(
        summary="Retrieve system activity logs retention settings",
        description="Get the current retention settings for system activity logs.",
    ),
    partial_update=extend_schema(
        summary="Update system activity logs retention settings and reschedule cleanup task",
        description="Update the retention settings for system activity logs and reschedule the cleanup task accordingly.",
    ),
)
class SystemActivityLogsRetentionViewSet(ListModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
    queryset = SystemActivityLogsRetention.objects.all()
    serializer_class = SystemActivityLogsRetentionSerializer

    @extend_schema(
        summary="Update system activity logs retention settings and reschedule cleanup task",
        description="Update the retention settings for system activity logs and reschedule the cleanup task accordingly.",
    )
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        sechedule_updated = update_cleanup_old_activity_logs_task(
            execution_interval_days=serializer.validated_data.get("retention_days")
        )
        if not sechedule_updated:
            return Response(
                {"message": "Failed to update the cleanup task."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(
    list=extend_schema(
        summary="Retrieve facial recognition activity logs retention settings",
        description="Get the current retention settings for facial recognition activity logs.",
    ),
    update=extend_schema(
        summary="Update facial recognition activity logs retention settings and reschedule cleanup task",
        description="Update the retention settings for facial recognition activity logs and reschedule the cleanup task accordingly.",
    ),
    partial_update=extend_schema(
        summary="Update facial recognition activity logs retention settings and reschedule cleanup task",
        description="Update the retention settings for facial recognition activity logs and reschedule the cleanup task accordingly.",
    ),
)
class FaceRecognitionActivityLogsRetentionViewSet(ListModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
    queryset = FaceRecognitionActivityLogsRetention.objects.all()
    serializer_class = FaceRecognitionActivityLogsRetentionSerializer
