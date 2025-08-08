from django.urls import include, path
from rest_framework import routers

from .views import (
    FaceRecognitionActivityLogsRetentionViewSet,
    FaceRecognitionActivityLogsViewSet,
    SystemActivityLogsRetentionViewSet,
    SystemActivityLogsViewSet,
)

activity_logs_router = routers.SimpleRouter()
activity_logs_router.register(
    r"api/activity-logs/system/retention", SystemActivityLogsRetentionViewSet, basename="system-activity-logs-retention"
)
activity_logs_router.register(r"api/activity-logs/system", SystemActivityLogsViewSet, basename="system-activity-logs")
activity_logs_router.register(
    r"api/activity-logs/face-recognition/retention",
    FaceRecognitionActivityLogsRetentionViewSet,
    basename="face-recognition-activity-logs-retention",
)
activity_logs_router.register(
    r"api/activity-logs/face-recognition", FaceRecognitionActivityLogsViewSet, basename="face-recognition-activity-logs"
)


urlpatterns = [
    path(r"", include(activity_logs_router.urls)),
]
