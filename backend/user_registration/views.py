from rest_framework import viewsets

from user_registration.filters import RegisterGroupFilter
from user_registration.models import RegisterGroup, RegisterUserProfile
from user_registration.serializers import (
    RegisterUserFeatureSerializer,
    RegisterUserProfileSerializer,
    UserRegistrationGroupSerializer,
)


class UserRegistrationViewSet(viewsets.ModelViewSet):
    queryset = RegisterUserProfile.objects.all()
    serializer_class = RegisterUserProfileSerializer


class RegisterUserFeatureViewSet(viewsets.ModelViewSet):
    queryset = RegisterUserProfile.objects.all()
    serializer_class = RegisterUserFeatureSerializer


class UserRegistrationGroupViewSet(viewsets.ModelViewSet):
    queryset = RegisterGroup.objects.all().order_by("group_name")
    serializer_class = UserRegistrationGroupSerializer
    filterset_class = RegisterGroupFilter
    filterset_fields = ["group_name"]
