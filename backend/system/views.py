import requests
from django.conf import settings
from rest_framework import status, viewsets
from rest_framework.mixins import ListModelMixin, UpdateModelMixin
from rest_framework.response import Response

from .models import DebugConfig, RecognitionConfig, VideoConfig
from .serializers import (
    FaceRecognitionConfigSerializer,
    FaceRecognitionDebugSerializer,
    VideoConfigSerializer,
)

MICROSERVICE_URL = settings.MICROSERVICE.get("URL", None)


class FaceRecognitionConfigViewSet(ListModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
    queryset = RecognitionConfig.objects.all()
    serializer_class = FaceRecognitionConfigSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if not MICROSERVICE_URL:
            return Response(
                {"error": "Microservice URL is not configured."}, status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        try:
            response = requests.post(MICROSERVICE_URL + "/api/face-reco-config/", json=serializer.validated_data)
            if response.status_code != 200:
                print("Error from microservice:", response.text)
                return Response(
                    {"error": "Failed to update microservice configuration."},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )
        except requests.RequestException as e:
            return Response(
                {"error": "Failed to connect to microservice.", "details": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VideoConfigViewSet(ListModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
    queryset = VideoConfig.objects.all()
    serializer_class = VideoConfigSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if not MICROSERVICE_URL:
            return Response(
                {"error": "Microservice URL is not configured."}, status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        try:
            response = requests.post(MICROSERVICE_URL + "/api/video-config/", json=serializer.validated_data)
            if response.status_code != 200:
                print("Error from microservice:", response.text)
                return Response(
                    {"error": "Failed to update microservice configuration."},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )
        except requests.RequestException as e:
            return Response(
                {"error": "Failed to connect to microservice.", "details": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PreviewViewSet(ListModelMixin, viewsets.GenericViewSet):
    queryset = RecognitionConfig.objects.all()
    serializer_class = []

    def list(self, request, *args, **kwargs):
        if not MICROSERVICE_URL:
            return Response(
                {"error": "Microservice URL is not configured."}, status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        try:
            response = requests.get(MICROSERVICE_URL + "/api/preview-camera/")
            if response.status_code != 200:
                print("Error from microservice:", response.text)
                return Response(
                    {"error": "Failed to fetch preview from microservice."},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )
            data = response.json()
            preview_image = data.get("preview_image_url", "")

            return Response({"image": preview_image}, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            return Response(
                {"error": "Failed to connect to microservice.", "details": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


class FaceRecognitionDebugViewSet(ListModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
    queryset = DebugConfig.objects.all()
    serializer_class = FaceRecognitionDebugSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if not MICROSERVICE_URL:
            return Response(
                {"error": "Microservice URL is not configured."}, status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        try:
            response = requests.post(MICROSERVICE_URL + "/api/debug/", json=serializer.validated_data)
            if response.status_code != 200:
                print("Error from microservice:", response.text)
                return Response(
                    {"error": "Failed to update microservice configuration."},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )
        except requests.RequestException as e:
            return Response(
                {"error": "Failed to connect to microservice.", "details": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
