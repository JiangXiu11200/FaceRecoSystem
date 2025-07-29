from accounts.models import UserProfile
from accounts.utils.verify_passward import format_check, make_hashed_password, verify_password
from rest_framework import serializers


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ["password"]


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


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True)
    new_password = serializers.CharField(max_length=128, write_only=True)

    def validate_old_password(self, value: str) -> str:
        user = self.context["user"]
        if not verify_password(value, user.password):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate_new_password(self, value: str) -> str:
        """Validate that new password meets security requirements."""
        user = self.context["user"]
        if verify_password(value, user.password):
            raise serializers.ValidationError("New password cannot be the same as the old password.")
        if not password_format_check(value):
            raise serializers.ValidationError("New password does not meet security requirements.")
        return value

    def save(self):
        user = self.context["user"]
        user.password = make_hashed_password(self.validated_data["new_password"])
        user.save()
        return user


def password_format_check(value: str) -> bool:
    """Check if the password meets security requirements."""
    is_valid, error_message = format_check(value)
    if is_valid:
        return value
    if error_message:
        raise serializers.ValidationError(error_message)
