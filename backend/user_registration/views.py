from rest_framework import viewsets

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
    queryset = RegisterGroup.objects.all()
    serializer_class = UserRegistrationGroupSerializer
