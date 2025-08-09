import os

# This is the ASGI config for the app_server project.
# Environment variables must be set before importing Django settings.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app_server.settings")  # noqa: E402

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from user_registration.streaming import routing

django_asgi_app = get_asgi_application()

from .streaming.middleware import JWTAuthMiddleware  # noqa: E402

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(JWTAuthMiddleware(URLRouter(routing.websocket_urlpatterns))),
    }
)
