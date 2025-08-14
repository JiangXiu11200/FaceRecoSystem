from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response

from .filters import AlarmLogsFilter
from .models import AlarmLogs
from .serializers import AcknowledgeAlarmLogsSerializer, AlarmLogsSerializer


class AlarmLogsViewSet(ListModelMixin, CreateModelMixin, viewsets.GenericViewSet):
    queryset = AlarmLogs.objects.all().order_by("-create_time")
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
            instance.acknowledged = True
            instance.save()
            return Response({"message": "Acknowledged."}, status=status.HTTP_200_OK)

        return Response({"message": "No changes made."}, status=status.HTTP_200_OK)

