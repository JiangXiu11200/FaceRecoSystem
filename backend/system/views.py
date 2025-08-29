import requests
from django.conf import settings
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response

from .models import DebugConfig, RecognitionConfig, VideoConfig
from .serializers import (
    FaceRecognitionConfigSerializer,
    FaceRecognitionDebugSerializer,
    VideoConfigSerializer,
)

MICROSERVICE_URL = settings.MICROSERVICE.get("endpoint", None)


@extend_schema_view(
    list=extend_schema(
        summary="List Configuration",
        description="Retrieve the current configuration settings.",
    ),
    update=extend_schema(
        summary="Update Configuration, ID is always 1",
        description="Update the configuration settings and propagate changes to the microservice.",
    ),
    retrive=extend_schema(
        summary="Retrieve Configuration, ID is always 1",
        description="Retrieve the configuration settings.",
    ),
    partial_update=extend_schema(
        summary="Partially Update Configuration, ID is always 1",
        description="Partially update the configuration settings and propagate changes to the microservice.",
    ),
)
class FaceRecognitionConfigViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
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


@extend_schema_view(
    list=extend_schema(
        summary="List Video Configuration",
        description="Retrieve the current video configuration settings.",
    ),
    update=extend_schema(
        summary="Update Video Configuration, ID is always 1",
        description="Update the video configuration settings and propagate changes to the microservice.",
    ),
    retrive=extend_schema(
        summary="Retrieve Video Configuration, ID is always 1",
        description="Retrieve the video configuration settings.",
    ),
    partial_update=extend_schema(
        summary="Partially Update Video Configuration, ID is always 1",
        description="Partially update the video configuration settings and propagate changes to the microservice.",
    ),
)
class VideoConfigViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
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


@extend_schema_view(
    list=extend_schema(
        summary="Get one preview image from the camera",
        description="Fetch a preview image from the camera via the microservice.",
        responses={200: {"type": "object", "properties": {"image": {"type": "string", "format": "uri"}}}},
    ),
)
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


@extend_schema_view(
    list=extend_schema(
        summary="List Debug Configuration",
        description="Retrieve the current debug configuration settings.",
    ),
    update=extend_schema(
        summary="Update Debug Configuration, ID is always 1",
        description="Update the debug configuration settings and propagate changes to the microservice.",
    ),
    partial_update=extend_schema(
        summary="Partially Update Debug Configuration, ID is always 1",
        description="Partially update the debug configuration settings and propagate changes to the microservice.",
    ),
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
