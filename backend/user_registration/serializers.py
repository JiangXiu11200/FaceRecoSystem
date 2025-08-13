import django_filters
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
        if request and request.method == "GET":
            self.fields.pop("face_details", None)
            self.fields["register_time"] = serializers.DateTimeField(read_only=True)
            self.fields["update_time"] = serializers.DateTimeField(read_only=True)
            self.fields["annotations"] = serializers.CharField(read_only=True, allow_blank=True, allow_null=True)
            self.fields["register_group"] = serializers.PrimaryKeyRelatedField(read_only=True)
            self.fields["register_group_name"] = serializers.CharField(
                source="register_group.group_name", read_only=True
            )

        elif request and request.method in ["PUT", "PATCH"]:
            self.fields["minio_key"].required = False
            self.fields["face_details"].required = False
            self.fields["file_name"].required = False


class RegisterUserProfileFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    register_group = django_filters.BaseInFilter(field_name="register_group", lookup_expr="in")

    class Meta:
        model = RegisterUserProfile
        fields = ["name", "register_group"]


class RegisterUserFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterUserProfile
        fields = ["id", "name", "face_details", "minio_key", "file_name"]


class UserRegistrationGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterGroup
        fields = "__all__"
