from rest_framework import serializers

from user_registration.models import RegisterGroup, RegisterUserProfile


class RegisterUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterUserProfile
        exclude = ["face_details"]


class RegisterUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterUserProfile
        fields = ["id", "name", "face_details", "minio_key", "file_name"]


class UserRegistrationGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterGroup
        fields = "__all__"
