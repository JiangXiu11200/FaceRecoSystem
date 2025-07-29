from django.db import models

_LEVEL_CHOICES = (
    (1, "Info"),
    (2, "Warning"),
    (3, "Critical"),
)


class AlarmLogs(models.Model):
    minio_key = models.CharField(max_length=128)
    file_name = models.CharField(max_length=128)
    acknowledged = models.BooleanField(default=False)
    alarm_type = models.IntegerField(choices=_LEVEL_CHOICES, default=1)
    alarm_message = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class AlarmLogsHistory(models.Model):
    minio_key = models.CharField(max_length=128)
    file_name = models.CharField(max_length=128)
    alarm_type = models.IntegerField(choices=_LEVEL_CHOICES, default=1)
    alarm_message = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField()
    acknowledged_time = models.DateTimeField(auto_now_add=True)
