from django.db import models

_LEVEL_CHOICES = (
    (1, "Info"),
    (2, "Warning"),
    (3, "Critical"),
    (4, "Error"),
    (5, "Fatal"),
)


class AlarmLogs(models.Model):
    minio_key = models.CharField(max_length=128)
    file_name = models.CharField(max_length=128)
    acknowledged = models.BooleanField(default=False)
    alarm_type = models.IntegerField(choices=_LEVEL_CHOICES, default=1)
    alarm_message = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
