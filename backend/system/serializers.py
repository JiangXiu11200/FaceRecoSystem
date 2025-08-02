from rest_framework import serializers

from .models import UserRecognitionConfig


class UserRecognitionConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRecognitionConfig
        fields = "__all__"


class UserRecognitionDebugSerializer(serializers.ModelSerializer):
    debug = serializers.BooleanField()

    class Meta:
        model = UserRecognitionConfig
        fields = ["debug"]
