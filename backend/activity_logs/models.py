from django.db import models


class SystemActivtiyLogs(models.Model):
    account = models.CharField(max_length=64)
    actions = models.CharField(max_length=8)
    status = models.BooleanField(default=True)
    status_code = models.IntegerField()
    message = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class FaceRecognitionActivityLogs(models.Model):
    account = models.CharField(max_length=64)
    actions = models.CharField(max_length=8)
    status = models.BooleanField(default=True)
    status_code = models.IntegerField()
    message = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class SystemActivityLogsRetention(models.Model):
    retention_days = models.IntegerField(default=90)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Retention Days: {self.retention_days}, Last Updated: {self.last_updated}"


class FaceRecognitionActivityLogsRetention(models.Model):
    retention_days = models.IntegerField(default=90)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Retention Days: {self.retention_days}, Last Updated: {self.last_updated}"
