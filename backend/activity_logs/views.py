from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.mixins import ListModelMixin, UpdateModelMixin
from rest_framework.response import Response

from activity_logs.utils.celery_scheduler_control import update_cleanup_old_activity_logs_task

from .filters import FaceRecognitionActivityLogsFilter
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
    queryset = SystemActivtiyLogs.objects.all()
    serializer_class = SystemActivityLogsSerializer


class FaceRecognitionActivityLogsViewSet(viewsets.ModelViewSet):
    queryset = FaceRecognitionActivityLogs.objects.all()
    serializer_class = FaceRecognitionActivityLogsSerializer
    filterset_class = FaceRecognitionActivityLogsFilter
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "group"]


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
