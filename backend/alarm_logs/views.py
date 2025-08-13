from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response

from .filters import AlarmLogsFilter
from .models import AlarmLogs, AlarmLogsHistory
from .serializers import AcknowledgeAlarmLogsSerializer, AlarmLogsHistorySerializer, AlarmLogsSerializer


class AlarmLogsViewSet(ListModelMixin, CreateModelMixin, viewsets.GenericViewSet):
    queryset = AlarmLogs.objects.all()
    serializer_class = AlarmLogsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AlarmLogsFilter


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
            AlarmLogsHistory.objects.create(
                minio_key=instance.minio_key,
                file_name=instance.file_name,
                alarm_type=instance.alarm_type,
                alarm_message=instance.alarm_message,
                create_time=instance.create_time,
            )
            instance.delete()
            return Response({"message": "Acknowledged."}, status=status.HTTP_200_OK)

        return Response({"message": "No changes made."}, status=status.HTTP_200_OK)


class AlarmLogsHistoryViewSet(ListModelMixin, CreateModelMixin, viewsets.GenericViewSet):
    queryset = AlarmLogs.objects.all()
    serializer_class = AlarmLogsHistorySerializer
