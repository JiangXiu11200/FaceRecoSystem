from django.db import models


class UserProfile(models.Model):
    account = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=128)
    keep_expiration_days = models.IntegerField(default=1)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=254)
    profile_picture_url = models.URLField(max_length=500, blank=True, null=True)
    description = models.TextField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    user_group = models.ForeignKey("UserGroup", related_name="users", on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.account:
            self.account = self.account.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.account


class UserGroup(models.Model):
    group_name = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    apps = models.ManyToManyField("SystemApps", related_name="user_groups", blank=True)


class SystemApps(models.Model):
    app_name = models.CharField(max_length=64, unique=True)
    label = models.CharField(max_length=64)
