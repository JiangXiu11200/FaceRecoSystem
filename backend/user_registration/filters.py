import django_filters

from user_registration.models import RegisterUserProfile

from .models import RegisterGroup


class RegisterGroupFilter(django_filters.FilterSet):
    group_name = django_filters.CharFilter(field_name="group_name", lookup_expr="icontains")

    class Meta:
        model = RegisterGroup
        fields = ["group_name"]


class RegisterUserProfileFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    register_group = django_filters.BaseInFilter(field_name="register_group", lookup_expr="in")

    class Meta:
        model = RegisterUserProfile
        fields = ["name", "register_group"]
