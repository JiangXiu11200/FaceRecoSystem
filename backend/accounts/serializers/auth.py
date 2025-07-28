from accounts.models import UserProfile
from accounts.utils.verify_passward import verify_password
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    account = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128, write_only=True)
    remember_me = serializers.BooleanField(default=False, write_only=True)

    def validate(self, attrs):
        login_account = attrs.get("account")
        login_password = attrs.get("password")

        if not login_account or not login_password:
            raise serializers.ValidationError("Account and password are required.")

        try:
            user_profile = UserProfile.objects.get(account__iexact=login_account)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError("Account does not exist.")

        if not verify_password(login_password, user_profile.password):
            raise serializers.ValidationError("Incorrect password.")

        return {
            "user_id": user_profile.id,
            "account": user_profile.account,
            "keep_expiration_days": user_profile.keep_expiration_days,
            "remember_me": attrs.get("remember_me"),
        }
