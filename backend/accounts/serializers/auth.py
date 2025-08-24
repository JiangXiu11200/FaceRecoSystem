from accounts.models import UserGroup, UserProfile
from accounts.utils.verify_passward import verify_password
from django.db.models import Prefetch
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    account = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128, write_only=True)
    remember_me = serializers.BooleanField(default=False, write_only=True)
    select_mode = serializers.CharField(max_length=8, write_only=True)

    def validate(self, attrs):
        login_account = attrs.get("account")
        login_password = attrs.get("password")
        select_mode = attrs.get("select_mode")

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
            "permissions": self.find_user_permissions(user_profile.id),
            "select_mode": select_mode,
            "account": user_profile.account,
            "keep_expiration_days": user_profile.keep_expiration_days,
            "remember_me": attrs.get("remember_me"),
            "is_active": user_profile.is_active,
            "group_active": user_profile.user_groups.filter(is_active=True).exists(),
            "profile_picture_file_name": user_profile.profile_picture_file_name,
        }

    def find_user_permissions(self, user_id: int) -> list[str]:
        """Return distinct app_name list derived from user's groups (prefetch)."""
        try:
            user = UserProfile.objects.prefetch_related(
                Prefetch("user_groups", queryset=UserGroup.objects.prefetch_related("apps"))
            ).get(id=user_id)
        except UserProfile.DoesNotExist:
            return []
        except Exception as e:
            raise serializers.ValidationError(f"Error retrieving user permissions: {str(e)}")

        if not user.user_groups.exists():
            return []
        app_names = {app.app_name for group in user.user_groups.all() for app in group.apps.all()}

        return sorted(app_names)
