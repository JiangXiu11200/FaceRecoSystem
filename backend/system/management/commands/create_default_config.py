from django.core.management.base import BaseCommand

from system.models import DebugConfig, RecognitionConfig, VideoConfig


class Command(BaseCommand):
    def handle(self, *args, **options):
        _, config_created = RecognitionConfig.objects.get_or_create(
            id=1,
            defaults={
                "enable_blink_detection": True,
                "dlib_predictor_path": "",
                "dlib_recognition_model_path": "",
                "face_model": "",
                "minimum_bounding_box_height": 0.0,
                "minimum_face_detection_score": 0.0,
                "eyes_detection_brightness_threshold": 0,
                "eyes_detection_brightness_value_min": 0,
                "eyes_detection_brightness_value_max": 0,
                "sensitivity": 0.5,
                "consecutive_prediction_intervals_frame": 90,
            },
        )
        if config_created:
            self.stdout.write(self.style.SUCCESS("Created default FaceRecognitionConfig"))
        else:
            self.stdout.write(self.style.WARNING("FaceRecognitionConfig already exists."))

        _, debug_created = DebugConfig.objects.get_or_create(id=1, defaults={"debug": False})
        if debug_created:
            self.stdout.write(self.style.SUCCESS("Created default FaceRecognitionDebug"))
        else:
            self.stdout.write(self.style.WARNING("FaceRecognitionDebug already exists."))

        _, video_created = VideoConfig.objects.get_or_create(
            id=1,
            defaults={
                "rtsp": "rtsp://",
                "web_camera": None,
                "image_height": 480,
                "image_width": 640,
                "detection_range_start_point_x": 0,
                "detection_range_start_point_y": 0,
                "detection_range_end_point_x": 0,
                "detection_range_end_point_y": 0,
            },
        )
        if video_created:
            self.stdout.write(self.style.SUCCESS("Created default VideoConfig"))
        else:
            self.stdout.write(self.style.WARNING("VideoConfig already exists."))
