import re

from accounts.models import UserProfile
from django.contrib.auth.hashers import make_password
from rest_framework import serializers


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"

    def validate_account(self, value):
        if UserProfile.objects.filter(account__iexact=value).exists():
            raise serializers.ValidationError("This account is already taken.")
        if len(value) < 5:
            raise serializers.ValidationError("Account name must be at least 8 characters long")
        return value.lower()

    def validate_password(self, value):
        """Validate that password meets security requirements."""

        validation_rules = [
            (r".{8,}", "Password must be at least 8 characters long"),
            (r"[A-Z]", "Password must contain at least one uppercase letter"),
            (r"[a-z]", "Password must contain at least one lowercase letter"),
            (r"\d", "Password must contain at least one digit"),
            (r"[\W_]", "Password must contain at least one special character"),
        ]
        for pattern, error_message in validation_rules:
            if not re.search(pattern, value):
                raise serializers.ValidationError(error_message)
        return value

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.pop("password", None)
        return rep

    def create(self, validated_data):
        validated_data["password"] = self.make_password(validated_data["password"])
        return super().create(validated_data)

    # def update(self, instance, validated_data):
    #     if "password" in validated_data:
    #         validated_data["password"] = self.make_password(validated_data["password"])
    #     return super().update(instance, validated_data)

    def make_password(self, value):
        """Hash the password before saving."""
        return make_password(value)
