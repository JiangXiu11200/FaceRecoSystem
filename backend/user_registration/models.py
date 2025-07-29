from django.db import models


class RegisterUserProfile(models.Model):
    name = models.CharField(max_length=64, unique=True)
    face_details = models.JSONField()
    minio_key = models.CharField(max_length=128)
    file_name = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    register_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    annotations = models.TextField(max_length=100, blank=True, null=True)
    register_group = models.ForeignKey(
        "RegisterGroup", related_name="registers", on_delete=models.SET_NULL, null=True, blank=True
    )


class RegisterGroup(models.Model):
    group_name = models.CharField(max_length=64, unique=True)
    user_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
