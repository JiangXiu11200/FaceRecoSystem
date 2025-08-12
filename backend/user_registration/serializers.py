from rest_framework import serializers

from user_registration.models import RegisterGroup, RegisterUserProfile


class RegisterUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterUserProfile
        fields = [
            "id",
            "name",
            "minio_key",
            "face_details",
            "file_name",
            "is_active",
            "register_group",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method in ["PUT", "PATCH"]:
            self.fields["minio_key"].required = False
            self.fields["face_details"].required = False
            self.fields["file_name"].required = False


class RegisterUserFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterUserProfile
        fields = ["id", "name", "face_details", "minio_key", "file_name"]


class UserRegistrationGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterGroup
        fields = "__all__"
