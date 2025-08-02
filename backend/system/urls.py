from django.urls import include, path
from rest_framework import routers

from .views import UserRecognitionConfigViewSet, UserRecognitionDebugViewSet

user_recognition_router = routers.SimpleRouter()
user_recognition_router.register(
    r"api/face-recognition-config/debug", UserRecognitionDebugViewSet, basename="user-recognition-debug"
)
user_recognition_router.register(
    r"api/face-recognition-config", UserRecognitionConfigViewSet, basename="user-recognition-config"
)


urlpatterns = [
    path(r"", include(user_recognition_router.urls)),
]
