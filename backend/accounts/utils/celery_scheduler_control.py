import json
import time

from django.utils import timezone
from django_celery_beat.models import CrontabSchedule, PeriodicTask


def update_s3_temporary_file_cleanup_task(run_at_startup: bool = True):
    """
    Create or update a Celery periodic task to clean up S3 temporary data.
    Executes daily at 00:00:00.
    Optionally runs once immediately at startup.
    """
    try:
        # Every day at midnight to clean up S3 temporary data
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute="0",
            hour="0",
            day_of_week="*",
            day_of_month="*",
            month_of_year="*",
            timezone=timezone.get_current_timezone_name(),
        )

        PeriodicTask.objects.update_or_create(
            name="cleanup_s3_temporary_data",
            defaults={
                "crontab": schedule,
                "task": "backend.accounts.tasks.cleanup_temporary_data",
                "args": json.dumps([]),
                "enabled": True,
            },
        )

        if run_at_startup:
            from accounts.tasks import cleanup_temporary_data

            time.sleep(5)
            cleanup_temporary_data.delay()

        return True
    except Exception as e:
        print(f"[Celery Scheduler Control Error] {e}")
        return False


def delete_s3_temporary_file_cleanup_task():
    try:
        deleted_count, _ = PeriodicTask.objects.filter(name="cleanup_s3_temporary_data").delete()
        print(f"Deleted {deleted_count} periodic tasks named 'cleanup_s3_temporary_data'.")
        return True
    except Exception as e:
        print(f"[Celery Scheduler Control Error] {e}")
        return False
