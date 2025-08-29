import requests
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from utils.minio_client import MinioClient

from user_registration.filters import RegisterGroupFilter
from user_registration.models import RegisterGroup, RegisterUserProfile
from user_registration.serializers import (
    RegisterUserProfileSerializer,
    UserRegistrationGroupSerializer,
)

from .filters import RegisterUserProfileFilter


@extend_schema_view(
    retrieve=extend_schema(
        summary="Retrieve Registered User",
        description="Retrieve the details of a registered user by their ID.",
    ),
    update=extend_schema(
        summary="Update Registered User",
        description="Update the details of a registered user.",
    ),
    partial_update=extend_schema(
        summary="Partially Update Registered User",
        description="Partially update the details of a registered user.",
    ),
)
class UserRegistrationViewSet(viewsets.ModelViewSet):
    queryset = RegisterUserProfile.objects.all().order_by("id")
    serializer_class = RegisterUserProfileSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    filter_backends = [DjangoFilterBackend]
    filterset_class = RegisterUserProfileFilter
    filterset_fields = ["name", "register_group"]

    @extend_schema(
        summary="List Registered Users",
        description="Retrieve a list of registered users along with their details and pre-signed URLs for their images.",
    )
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

    @extend_schema(
        summary="Register a New User",
        description="Register a new user and post their image to an external microservice.",
        request={
            "application/json": {
                "properties": {
                    "name": {"type": "string"},
                    "register_group": {"type": "integer"},
                    "image": {"type": "string", "description": "Base64 encoded face image"},
                },
            }
        },
    )
    def create(self, request):
        name = request.data.get("name")
        register_group = request.data.get("register_group")
        image = request.data.get("image")

        if not name or not register_group or not image:
            return Response(
                {"error": "Name, register group, and image are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        microservice_url = settings.MICROSERVICE.get("endpoint", None)
        if not microservice_url:
            return Response(
                {"error": "Microservice URL is not configured."}, status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        # TODO: 重構將其呼叫方法獨立成一個模組
        try:
            response = requests.post(
                microservice_url + "/api/register-face",
                data={"name": name, "base64_face_image": image},
            )

            if response.status_code != 201:
                print("Error from microservice:", response.json())
                return Response(
                    {"error": "Service exception, please try again later."},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )
        except requests.exceptions.RequestException as e:
            print("Request to microservice failed:", str(e))
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

    @extend_schema(
        summary="Delete a Registered User",
        description="Delete a registered user and notify the external microservice to remove their data.",
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        name = instance.name
        microservice_url = settings.MICROSERVICE.get("endpoint", None)

        response = requests.post(
            microservice_url + f"/api/delete-registered-face/{name}",
        )
        if response.status_code != 200:
            print("Error from microservice:", response.json())
            return Response(
                {"error": "Service exception, please try again later."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return super().destroy(request, *args, **kwargs)

    # TODO: 新增 update 方法，當使用者更新圖片時，也要 call microservice 更新用戶名稱
    # def update(self, request, *args, **kwargs):
    #     ...


@extend_schema_view(
    list=extend_schema(
        summary="List User Registration Groups",
        description="Retrieve a list of user registration groups along with their details.",
    ),
    create=extend_schema(
        summary="Create User Registration Group",
        description="Create a new user registration group.",
    ),
    retrieve=extend_schema(
        summary="Retrieve User Registration Group",
        description="Retrieve the details of a user registration group by its ID.",
    ),
    update=extend_schema(
        summary="Update User Registration Group",
        description="Update the details of a user registration group.",
    ),
    partial_update=extend_schema(
        summary="Partially Update User Registration Group",
        description="Partially update the details of a user registration group.",
    ),
    destroy=extend_schema(
        summary="Delete User Registration Group",
        description="Delete a user registration group.",
    ),
)
class UserRegistrationGroupViewSet(viewsets.ModelViewSet):
    queryset = RegisterGroup.objects.all().order_by("group_name")
    serializer_class = UserRegistrationGroupSerializer
    filterset_class = RegisterGroupFilter
    filterset_fields = ["group_name"]
