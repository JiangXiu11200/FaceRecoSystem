import os

from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from user_registration.filters import RegisterGroupFilter
from user_registration.models import RegisterGroup, RegisterUserProfile
from user_registration.serializers import (
    RegisterUserFeatureSerializer,
    RegisterUserProfileSerializer,
    UserRegistrationGroupSerializer,
)

from .filters import RegisterUserProfileFilter


class UserRegistrationViewSet(viewsets.ModelViewSet):
    queryset = RegisterUserProfile.objects.all().order_by("id")
    serializer_class = RegisterUserProfileSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    filter_backends = [DjangoFilterBackend]
    filterset_class = RegisterUserProfileFilter
    filterset_fields = ["name", "register_group"]

    def create(self, request):
        name = request.data.get("name")
        register_group = request.data.get("register_group")
        image = request.FILES.get("image")

        if not name or not register_group or not image:
            return Response(
                {"error": "Name, register group, and image are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # TODO: 將二進制圖片傳給 Microservice 做特徵擷取
        image_path = settings.SCREENSHOT_OUTPUT_PATH + os.sep + image.name
        os.makedirs(settings.SCREENSHOT_OUTPUT_PATH, exist_ok=True)
        with open(image_path, "wb") as f:
            for chunk in image.chunks():
                f.write(chunk)
        # response = requests.post(
        #     settings.MICROSERVICE_URL + "/api/feature-extraction",
        #     files={"image": open(image_path, "rb")},
        #     data={"user_name": user_name, "group": group},
        # )
        # face_details = call_microservice(image_path)  # 回傳 dict
        face_details = {"test": "face details"}  # 範例用

        serializer = self.get_serializer(
            data={
                "name": name,
                "face_details": face_details,
                "minio_key": "http://example.com/minio_key",
                "file_name": f"{name}_{register_group}.jpg",
                "is_active": True,
                "register_group": register_group,
            }
        )

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # TODO: Delete MinIO file when user is deleted
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterUserFeatureViewSet(viewsets.ModelViewSet):
    queryset = RegisterUserProfile.objects.all()
    serializer_class = RegisterUserFeatureSerializer


class UserRegistrationGroupViewSet(viewsets.ModelViewSet):
    queryset = RegisterGroup.objects.all().order_by("group_name")
    serializer_class = UserRegistrationGroupSerializer
    filterset_class = RegisterGroupFilter
    filterset_fields = ["group_name"]
