from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.mixins import ListModelMixin, UpdateModelMixin
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


class SystemActivityLogsViewSet(viewsets.ModelViewSet):
    queryset = SystemActivtiyLogs.objects.all().order_by("-timestamp")
    serializer_class = SystemActivityLogsSerializer
    filterset_class = SystemActivityLogsFilter
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["account"]


class FaceRecognitionActivityLogsViewSet(viewsets.ModelViewSet):
    queryset = FaceRecognitionActivityLogs.objects.all()
    serializer_class = FaceRecognitionActivityLogsSerializer
    filterset_class = FaceRecognitionActivityLogsFilter
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "group"]

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


class SystemActivityLogsRetentionViewSet(ListModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
    queryset = SystemActivityLogsRetention.objects.all()
    serializer_class = SystemActivityLogsRetentionSerializer

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


class FaceRecognitionActivityLogsRetentionViewSet(ListModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
    queryset = FaceRecognitionActivityLogsRetention.objects.all()
    serializer_class = FaceRecognitionActivityLogsRetentionSerializer
