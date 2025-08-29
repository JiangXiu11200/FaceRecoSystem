from rest_framework import serializers

from .models import DebugConfig, RecognitionConfig, VideoConfig


class FaceRecognitionConfigSerializer(serializers.ModelSerializer):
    enable_blink_detection = serializers.BooleanField(default=True, help_text="Enable blink detection")
    dlib_predictor_path = serializers.CharField(
        default="", max_length=256, allow_blank=True, help_text="Path to the Dlib predictor model"
    )
    dlib_recognition_model_path = serializers.CharField(
        default="", max_length=256, allow_blank=True, help_text="Path to the Dlib recognition model"
    )
    face_model = serializers.CharField(
        default="", max_length=256, allow_blank=True, help_text="CSV model file for face features"
    )
    minimum_bounding_box_height = serializers.FloatField(
        default=0.0, min_value=0.0, max_value=1.0, help_text="Minimum bounding box height as a ratio (0.0 to 1.0)"
    )
    minimum_face_detection_score = serializers.FloatField(
        default=0.0, min_value=0.0, max_value=1.0, help_text="Minimum face detection score as a ratio (0.0 to 1.0)"
    )
    eyes_detection_brightness_threshold = serializers.IntegerField(
        default=0, min_value=0, max_value=255, help_text="Brightness threshold for eyes detection"
    )
    eyes_detection_brightness_value_min = serializers.IntegerField(
        default=0, min_value=0, max_value=255, help_text="Minimum brightness value for eyes detection"
    )
    eyes_detection_brightness_value_max = serializers.IntegerField(
        default=0, min_value=0, max_value=255, help_text="Maximum brightness value for eyes detection"
    )
    sensitivity = serializers.FloatField(
        default=0.5, min_value=0.0, max_value=1.0, help_text="Sensitivity for face detection (0.0 to 1.0)"
    )
    consecutive_prediction_intervals_frame = serializers.IntegerField(
        default=90, min_value=10, max_value=150, help_text="Number of frames for consecutive predictions (10 to 150)"
    )

    class Meta:
        model = RecognitionConfig
        fields = "__all__"


class VideoConfigSerializer(serializers.ModelSerializer):
    rtsp = serializers.CharField(
        required=False,
        allow_null=True,
        max_length=64,
        allow_blank=True,
        help_text="RTSP stream URL (if not None, use RTSP stream)",
    )
    web_camera = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text="Web camera index (if not None, use web camera)",
    )
    image_height = serializers.IntegerField(
        default=480, min_value=0, max_value=2160, help_text="Resize height of the input image"
    )
    image_width = serializers.IntegerField(
        default=640, min_value=0, max_value=3840, help_text="Resize width of the input image"
    )
    detection_range_start_point_x = serializers.IntegerField(
        default=0, min_value=0, max_value=3840, help_text="X coordinate of the start point of the detection range"
    )
    detection_range_start_point_y = serializers.IntegerField(
        default=0, min_value=0, max_value=2160, help_text="Y coordinate of the start point of the detection range"
    )
    detection_range_end_point_x = serializers.IntegerField(
        default=0, min_value=0, max_value=3840, help_text="X coordinate of the end point of the detection range"
    )
    detection_range_end_point_y = serializers.IntegerField(
        default=0, min_value=0, max_value=2160, help_text="Y coordinate of the end point of the detection range"
    )

    class Meta:
        model = VideoConfig
        fields = "__all__"


class FaceRecognitionDebugSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebugConfig
        fields = "__all__"
