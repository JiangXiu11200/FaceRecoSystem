from django_filters import rest_framework as django_filters

from .models import UserProfile


class AccountsFilter(django_filters.FilterSet):
    account = django_filters.CharFilter(field_name="account", lookup_expr="icontains")

    class Meta:
        model = UserProfile
        fields = ["account"]
