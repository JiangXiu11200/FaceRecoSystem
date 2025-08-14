from django.urls import include, path
from rest_framework import routers

from .views import AcknowledgeAlarmLogsViewSet, AlarmLogsViewSet

alarm_logs = routers.SimpleRouter()
alarm_logs.register(r"api/alarm-logs/acknowledge", AcknowledgeAlarmLogsViewSet, basename="alarmlogs-acknowledge")
alarm_logs.register(r"api/alarm-logs", AlarmLogsViewSet, basename="alarmlogs")


urlpatterns = [
    path(r"", include(alarm_logs.urls)),
]
