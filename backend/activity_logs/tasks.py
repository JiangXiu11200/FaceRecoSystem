from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from .models import SystemActivtiyLogs


@shared_task
def cleanup_old_activity_logs(retention_days: int = 90):
    """Setting up scheduled tasks with Celery, this function will be cleaning up old activity logs."""
    cutoff = now() - timedelta(days=retention_days)

    deleted_count, _ = SystemActivtiyLogs.objects.filter(timestamp__lt=cutoff).delete()
    return f"Deleted {deleted_count} logs older than {retention_days} days"
