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

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        urls = self.context.get("minio_urls", {})
        s3_object_key = rep.get("s3_object_key")
        if s3_object_key and s3_object_key in urls:
            rep["minio_urls"] = urls[s3_object_key]
        return rep


class SystemActivityLogsRetentionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemActivityLogsRetention
        fields = "__all__"


class FaceRecognitionActivityLogsRetentionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceRecognitionActivityLogsRetention
        fields = "__all__"
