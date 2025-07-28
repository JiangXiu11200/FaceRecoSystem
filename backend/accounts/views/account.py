from accounts.models import UserProfile
from accounts.serializers.account import UserRegisterSerializer
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet


class RegisterViewSet(CreateModelMixin, GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserRegisterSerializer
