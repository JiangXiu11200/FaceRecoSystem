from accounts.models import UserProfile
from accounts.utils.verify_passward import format_check, make_hashed_password
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
        return password_format_check(value)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.pop("password", None)
        return rep

    def create(self, validated_data):
        validated_data["password"] = make_hashed_password(validated_data["password"])
        return super().create(validated_data)


def password_format_check(value: str) -> bool:
    """Check if the password meets security requirements."""
    is_valid, error_message = format_check(value)
    if is_valid:
        return value
    if error_message:
        raise serializers.ValidationError(error_message)
