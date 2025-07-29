from django.urls import include, path
from rest_framework import routers

from .views import AcknowledgeAlarmLogsViewSet, AlarmLogsHistoryViewSet, AlarmLogsViewSet

alarm_logs = routers.SimpleRouter()
alarm_logs.register(r"api/alarmlogs/history", AlarmLogsHistoryViewSet, basename="alarmlogs-history")
alarm_logs.register(r"api/alarmlogs/acknowledge", AcknowledgeAlarmLogsViewSet, basename="alarmlogs-acknowledge")
alarm_logs.register(r"api/alarmlogs", AlarmLogsViewSet, basename="alarmlogs")


urlpatterns = [
    path(r"", include(alarm_logs.urls)),
]
