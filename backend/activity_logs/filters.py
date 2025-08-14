from django_filters import rest_framework as filters

from .models import FaceRecognitionActivityLogs, SystemActivtiyLogs


class FaceRecognitionActivityLogsFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    group = filters.CharFilter(field_name="group", lookup_expr="icontains")

    class Meta:
        model = FaceRecognitionActivityLogs
        fields = ["name", "group"]


class SystemActivityLogsFilter(filters.FilterSet):
    account = filters.CharFilter(field_name="account", lookup_expr="icontains")

    class Meta:
        model = SystemActivtiyLogs
        fields = ["account"]
