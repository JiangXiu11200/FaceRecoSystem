from rest_framework import serializers

from .models import DebugConfig, RecognitionConfig, VideoConfig


class FaceRecognitionConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecognitionConfig
        fields = "__all__"


class VideoConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoConfig
        fields = "__all__"


class FaceRecognitionDebugSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebugConfig
        fields = "__all__"
