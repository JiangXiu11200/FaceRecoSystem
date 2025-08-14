from django_filters import rest_framework as filters

from .models import AlarmLogs


class AlarmLogsFilter(filters.FilterSet):
    alarm_category = filters.BaseInFilter(field_name="alarm_type", lookup_expr="in")
    start_date = filters.DateTimeFilter(field_name="create_time", lookup_expr="gte")
    end_date = filters.DateTimeFilter(field_name="create_time", lookup_expr="lte")
    acknowledged = filters.BooleanFilter(field_name="acknowledged", method="filter_acknowledged")

    class Meta:
        model = AlarmLogs
        fields = ["alarm_category", "start_date", "end_date", "acknowledged"]

    def filter_acknowledged(self, queryset, name, value):
        if value is True:
            return queryset.filter(acknowledged=True)
        elif value is False:
            return queryset.filter(acknowledged=False)
        return queryset
