from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class SystemActivtiyLogs(models.Model):
    account = models.CharField(max_length=64)
    actions = models.CharField(max_length=8)
    status = models.BooleanField(default=True)
    status_code = models.IntegerField()
    activity = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class FaceRecognitionActivityLogs(models.Model):
    name = models.CharField(max_length=64)
    group = models.CharField(
        max_length=64, blank=True, null=True
    )  # 預留欄位。當前 face recognition app 尚無同步 group ID
    s3_object_key = models.CharField(max_length=128, blank=True, null=True)
    detection_results = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


class SystemActivityLogsRetention(models.Model):
    retention_days = models.IntegerField(default=90, validators=[MinValueValidator(1), MaxValueValidator(365)])
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Retention Days: {self.retention_days}, Last Updated: {self.last_updated}"


class FaceRecognitionActivityLogsRetention(models.Model):
    retention_days = models.IntegerField(default=90, validators=[MinValueValidator(1), MaxValueValidator(365)])
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Retention Days: {self.retention_days}, Last Updated: {self.last_updated}"
