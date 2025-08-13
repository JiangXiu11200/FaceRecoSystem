from django_filters import rest_framework as filters

from .models import AlarmLogs


class AlarmLogsFilter(filters.FilterSet):
    alarm_category = filters.BaseInFilter(field_name="alarm_type", lookup_expr="in")
    start_date = filters.DateTimeFilter(field_name="create_time", lookup_expr="gte")
    end_date = filters.DateTimeFilter(field_name="create_time", lookup_expr="lte")

    class Meta:
        model = AlarmLogs
        fields = ["alarm_category", "start_date", "end_date"]
