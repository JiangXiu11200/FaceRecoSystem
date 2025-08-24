from django.db import models


class DebugConfig(models.Model):
    debug = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


class VideoConfig(models.Model):
    rtsp = models.CharField(default="", max_length=256, blank=True)
    web_camera = models.IntegerField(null=True, blank=True)
    image_height = models.IntegerField()
    image_width = models.IntegerField()
    detection_range_start_point_x = models.IntegerField()
    detection_range_start_point_y = models.IntegerField()
    detection_range_end_point_x = models.IntegerField()
    detection_range_end_point_y = models.IntegerField()

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


class RecognitionConfig(models.Model):
    enable_blink_detection = models.BooleanField(default=True)
    dlib_predictor_path = models.CharField(max_length=256, default="")
    dlib_recognition_model_path = models.CharField(max_length=256, default="")
    face_model = models.CharField(max_length=256, default="")  # TODO: Change to key value db
    minimum_bounding_box_height = models.FloatField(default=0.0)
    minimum_face_detection_score = models.FloatField(default=0.0)
    eyes_detection_brightness_threshold = models.IntegerField(default=0)
    eyes_detection_brightness_value_min = models.IntegerField(default=0)
    eyes_detection_brightness_value_max = models.IntegerField(default=0)
    sensitivity = models.FloatField(default=0.5)
    consecutive_prediction_intervals_frame = models.IntegerField(default=90)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
