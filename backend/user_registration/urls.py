from django.urls import include, path
from rest_framework import routers

from user_registration.views import RegisterUserDetailsViewSet, UserRegistrationGroupViewSet, UserRegistrationViewSet

user_registration_router = routers.SimpleRouter()
user_registration_router.register(
    r"api/user-registration/group", UserRegistrationGroupViewSet, basename="user-registration-group"
)
user_registration_router.register(
    r"api/user-registration/details", RegisterUserDetailsViewSet, basename="user-registration-details"
)
user_registration_router.register(r"api/user-registration", UserRegistrationViewSet, basename="user-registration")


urlpatterns = [
    path(r"", include(user_registration_router.urls)),
]
