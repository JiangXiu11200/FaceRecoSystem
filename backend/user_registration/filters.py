import django_filters

from .models import RegisterGroup


class RegisterGroupFilter(django_filters.FilterSet):
    group_name = django_filters.CharFilter(field_name="group_name", lookup_expr="icontains")

    class Meta:
        model = RegisterGroup
        fields = ["group_name"]
