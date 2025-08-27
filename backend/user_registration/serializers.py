from rest_framework import serializers

from user_registration.models import RegisterGroup, RegisterUserProfile


class RegisterUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterUserProfile
        fields = [
            "id",
            "name",
            "s3_object_key",
            "is_active",
            "register_group",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "GET":
            self.fields["register_time"] = serializers.DateTimeField(read_only=True)
            self.fields["update_time"] = serializers.DateTimeField(read_only=True)
            self.fields["annotations"] = serializers.CharField(read_only=True, allow_blank=True, allow_null=True)
            self.fields["register_group"] = serializers.PrimaryKeyRelatedField(read_only=True)
            self.fields["register_group_name"] = serializers.CharField(
                source="register_group.group_name", read_only=True
            )

        elif request and request.method in ["PUT", "PATCH"]:
            self.fields["s3_object_key"].required = False

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        urls = self.context.get("minio_urls", {})
        s3_object_key = rep.get("s3_object_key")
        if s3_object_key and s3_object_key in urls:
            rep["register_picture_url"] = urls[s3_object_key]
        return rep


class UserRegistrationGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterGroup
        fields = "__all__"
