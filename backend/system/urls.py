from django.urls import include, path
from rest_framework import routers

from .views import (
    FaceRecognitionConfigViewSet,
    FaceRecognitionDebugViewSet,
    PreviewViewSet,
    VideoConfigViewSet,
)

user_recognition_router = routers.SimpleRouter()
user_recognition_router.register(
    r"api/face-recognition-config/debug", FaceRecognitionDebugViewSet, basename="user-recognition-debug"
)
user_recognition_router.register(
    r"api/face-recognition-config/preview", PreviewViewSet, basename="user-recognition-preview"
)
user_recognition_router.register(
    r"api/face-recognition-config/video", VideoConfigViewSet, basename="face-recognition-video-config"
)
user_recognition_router.register(
    r"api/face-recognition-config/recognition",
    FaceRecognitionConfigViewSet,
    basename="face-recognition-recognition-config",
)

urlpatterns = [
    path(r"", include(user_recognition_router.urls)),
]
