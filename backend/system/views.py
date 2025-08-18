from rest_framework import status, viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response

from .models import UserRecognitionConfig
from .serializers import UserRecognitionConfigSerializer, UserRecognitionDebugSerializer


class UserRecognitionConfigViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
    queryset = UserRecognitionConfig.objects.all()
    serializer_class = UserRecognitionConfigSerializer

class UserRecognitionConfigPreviewViewSet(ListModelMixin, viewsets.GenericViewSet):
    queryset = UserRecognitionConfig.objects.all()
    serializer_class = []

    def list(self, request, *args, **kwargs):
        # TODO: Call Microservice API to get the image preview
        return Response({"error": "Preview not implemented yet"}, status=status.HTTP_501_NOT_IMPLEMENTED)

class UserRecognitionDebugViewSet(ListModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
    queryset = UserRecognitionConfig.objects.all()
    serializer_class = UserRecognitionDebugSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # TODO: Added restart microservice logic here.

        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
