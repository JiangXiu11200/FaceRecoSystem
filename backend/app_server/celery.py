import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app_server.settings")

app = Celery("app_server")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
