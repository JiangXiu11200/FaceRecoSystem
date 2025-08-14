from rest_framework import serializers

from .models import AlarmLogs


class AlarmLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlarmLogs
        fields = "__all__"


class AcknowledgeAlarmLogsSerializer(serializers.ModelSerializer):
    acknowledged = serializers.BooleanField(required=True)

    class Meta:
        model = AlarmLogs
        fields = ["acknowledged"]
