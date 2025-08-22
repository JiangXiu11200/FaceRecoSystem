import requests
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from utils.minio_client import MinioClient

from user_registration.filters import RegisterGroupFilter
from user_registration.models import RegisterGroup, RegisterUserProfile
from user_registration.serializers import (
    RegisterUserFeatureSerializer,
    RegisterUserProfileSerializer,
    UserRegistrationGroupSerializer,
)

from .filters import RegisterUserProfileFilter

MICROSERVICE_URL = settings.MICROSERVICE.get("URL", None)


class UserRegistrationViewSet(viewsets.ModelViewSet):
    queryset = RegisterUserProfile.objects.all().order_by("id")
    serializer_class = RegisterUserProfileSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    filter_backends = [DjangoFilterBackend]
    filterset_class = RegisterUserProfileFilter
    filterset_fields = ["name", "register_group"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        object_names = [obj.s3_object_key for obj in (page or queryset) if obj.s3_object_key]
        urls = {}

        if object_names:
            try:
                state, results = MinioClient.get_multiple_objects_url(
                    bucket_name="user-registration",
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

    def create(self, request):
        name = request.data.get("name")
        register_group = request.data.get("register_group")
        image = request.data.get("image")

        if not name or not register_group or not image:
            return Response(
                {"error": "Name, register group, and image are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not MICROSERVICE_URL:
            return Response(
                {"error": "Microservice URL is not configured."}, status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        # TODO: 重構將其呼叫方法獨立成一個模組
        response = requests.post(
            MICROSERVICE_URL + "/api/register-face",
            data={"name": name, "base64_face_image": image},
        )

        if response.status_code != 201:
            print("Error from microservice:", response.json())
            return Response(
                {"error": "Service exception, please try again later."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        response = response.json()
        serializer = self.get_serializer(
            data={
                "name": name,
                "s3_object_key": response.get("s3_object_key"),
                "is_active": True,
                "register_group": register_group,
            }
        )

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        name = instance.name

        response = requests.post(
            MICROSERVICE_URL + f"/api/delete-registered-face/{name}",
        )
        if response.status_code != 200:
            print("Error from microservice:", response.json())
            return Response(
                {"error": "Service exception, please try again later."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return super().destroy(request, *args, **kwargs)


class RegisterUserFeatureViewSet(viewsets.ModelViewSet):
    queryset = RegisterUserProfile.objects.all()
    serializer_class = RegisterUserFeatureSerializer


class UserRegistrationGroupViewSet(viewsets.ModelViewSet):
    queryset = RegisterGroup.objects.all().order_by("group_name")
    serializer_class = UserRegistrationGroupSerializer
    filterset_class = RegisterGroupFilter
    filterset_fields = ["group_name"]
