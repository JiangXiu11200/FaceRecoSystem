from rest_framework import serializers

from .models import (
    FaceRecognitionActivityLogs,
    FaceRecognitionActivityLogsRetention,
    SystemActivityLogsRetention,
    SystemActivtiyLogs,
)


class SystemActivityLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemActivtiyLogs
        fields = "__all__"


class FaceRecognitionActivityLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceRecognitionActivityLogs
        fields = "__all__"


class SystemActivityLogsRetentionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemActivityLogsRetention
        fields = "__all__"


class FaceRecognitionActivityLogsRetentionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceRecognitionActivityLogsRetention
        fields = "__all__"
