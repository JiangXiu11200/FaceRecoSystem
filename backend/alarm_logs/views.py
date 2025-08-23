from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from utils.minio_client import MinioClient

from .filters import AlarmLogsFilter
from .models import AlarmLogs
from .serializers import AcknowledgeAlarmLogsSerializer, AlarmLogsSerializer


class AlarmLogsViewSet(ListModelMixin, CreateModelMixin, viewsets.GenericViewSet):
    queryset = AlarmLogs.objects.all().order_by("-timestamp")
    serializer_class = AlarmLogsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AlarmLogsFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        object_names = [obj.s3_object_key for obj in (page or queryset) if obj.s3_object_key]
        urls = {}

        if object_names:
            try:
                state, results = MinioClient.get_multiple_objects_url(
                    bucket_name="face-alarm-logs",
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

class AcknowledgeAlarmLogsViewSet(UpdateModelMixin, viewsets.GenericViewSet):
    queryset = AlarmLogs.objects.all()
    serializer_class = AcknowledgeAlarmLogsSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        acknowledged = serializer.validated_data.get("acknowledged", False)
        if acknowledged and not instance.acknowledged:
            instance.acknowledged = True
            instance.save()
            return Response({"message": "Acknowledged."}, status=status.HTTP_200_OK)

        return Response({"message": "No changes made."}, status=status.HTTP_200_OK)
