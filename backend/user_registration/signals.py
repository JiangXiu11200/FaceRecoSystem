from django.db.models.signals import post_save, pre_save
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
    """儲存時更新群組計數"""
    old_group = getattr(instance, "_old_group", None)
    new_group = instance.register_group

    # 如果是新建立的使用者
    if created:
        if new_group:
            new_group.user_count += 1
            new_group.save(update_fields=["user_count"])

    # 如果是更新且群組有變更
    elif old_group != new_group:
        # 從舊群組減少計數
        if old_group:
            old_group.user_count = max(0, old_group.user_count - 1)
            old_group.save(update_fields=["user_count"])

        # 新群組增加計數
        if new_group:
            new_group.user_count += 1
            new_group.save(update_fields=["user_count"])
