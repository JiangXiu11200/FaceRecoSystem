from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, UpdateModelMixin

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


class SystemActivityLogsRetentionViewSet(ListModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
    queryset = SystemActivityLogsRetention.objects.all()
    serializer_class = SystemActivityLogsRetentionSerializer


class FaceRecognitionActivityLogsRetentionViewSet(ListModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
    queryset = FaceRecognitionActivityLogsRetention.objects.all()
    serializer_class = FaceRecognitionActivityLogsRetentionSerializer
