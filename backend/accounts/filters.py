from django_filters import rest_framework as django_filters

from .models import UserGroup, UserProfile


class AccountsFilter(django_filters.FilterSet):
    account = django_filters.CharFilter(field_name="account", lookup_expr="icontains")

    class Meta:
        model = UserProfile
        fields = ["account"]


class AccountsGroupFilter(django_filters.FilterSet):
    group_name = django_filters.CharFilter(field_name="group_name", lookup_expr="icontains")

    class Meta:
        model = UserGroup
        fields = ["group_name"]
