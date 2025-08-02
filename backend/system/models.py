from django.db import models


class UserRecognitionConfig(models.Model):
    debug = models.BooleanField(default=False)
    rtsp = models.CharField(max_length=256, unique=True)
    image_height = models.IntegerField()
    image_width = models.IntegerField()
    dlib_predicotr_path = models.CharField(max_length=256)
    dlib_recognition_model_path = models.CharField(max_length=256)
    detection_range_start_point_x = models.IntegerField()
    detection_range_start_point_y = models.IntegerField()
    detection_range_end_point_x = models.IntegerField()
    detection_range_end_point_y = models.IntegerField()
    minimum_bounding_box_height = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    minimum_face_detection_score = models.DecimalField(max_digits=2, decimal_places=1, default=0.6)
    eyes_detection_brightness_threshold = models.IntegerField()
    eyes_detection_brightness_value_min = models.IntegerField()
    eyes_detection_brightness_value_max = models.IntegerField()
    sensitivity = models.DecimalField(max_digits=2, decimal_places=1, default=0.4)
    consecutive_prediction_intervals_frame = models.IntegerField(default=90)
