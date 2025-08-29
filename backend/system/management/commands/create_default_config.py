from django.core.management.base import BaseCommand

from system.models import DebugConfig, RecognitionConfig, VideoConfig


class Command(BaseCommand):
    def handle(self, *args, **options):
        _, config_created = RecognitionConfig.objects.get_or_create(
            id=1,
            defaults={
                "enable_blink_detection": True,
                "dlib_predictor_path": "models/dlib/shape_predictor_68_face_landmarks.dat",
                "dlib_recognition_model_path": "models/dlib/dlib_face_recognition_resnet_model_v1.dat",
                "face_model": "models/face_recognition/model.csv",
                "minimum_bounding_box_height": 0.4,
                "minimum_face_detection_score": 0.6,
                "eyes_detection_brightness_threshold": 120,
                "eyes_detection_brightness_value_min": 50,
                "eyes_detection_brightness_value_max": 20,
                "sensitivity": 0.4,
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
                "rtsp": "",
                "web_camera": 0,
                "image_height": 720,
                "image_width": 1280,
                "detection_range_start_point_x": 420,
                "detection_range_start_point_y": 160,
                "detection_range_end_point_x": 820,
                "detection_range_end_point_y": 560,
            },
        )
        if video_created:
            self.stdout.write(self.style.SUCCESS("Created default VideoConfig"))
        else:
            self.stdout.write(self.style.WARNING("VideoConfig already exists."))
