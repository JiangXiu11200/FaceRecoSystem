from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from user_registration.models import RegisterUserProfile


# Signal handlers
@receiver(pre_save, sender=RegisterUserProfile)
def track_group_change(sender, instance, **kwargs):
    """追蹤群組變更"""
    if instance.pk:  # 如果是更新（不是新建）
        try:
            old_instance = RegisterUserProfile.objects.get(pk=instance.pk)
            instance._old_group = old_instance.register_group
        except RegisterUserProfile.DoesNotExist:
            instance._old_group = None
    else:
        instance._old_group = None


@receiver(post_save, sender=RegisterUserProfile)
def update_group_count_on_save(sender, instance, created, **kwargs):
    """Update user count in the group when a user is created or updated."""
    old_group = getattr(instance, "_old_group", None)
    new_group = instance.register_group
    print(f"Old Group: {old_group}, New Group: {new_group}")

    # Create new user
    if created:
        if new_group:
            new_group.user_count += 1
            new_group.save(update_fields=["user_count"])

    # Update existing user
    elif old_group != new_group:
        if old_group:
            old_group.user_count = max(0, old_group.user_count - 1)
            old_group.save(update_fields=["user_count"])

        if new_group:
            new_group.user_count += 1
            new_group.save(update_fields=["user_count"])


@receiver(pre_delete, sender=RegisterUserProfile)
def delete_user_profile(sender, instance, **kwargs):
    """Delete user profile and update group count."""
    group = instance.register_group
    if group:
        group.user_count = max(0, group.user_count - 1)
        group.save(update_fields=["user_count"])
