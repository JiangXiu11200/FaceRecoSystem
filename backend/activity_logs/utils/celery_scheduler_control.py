import json

from django_celery_beat.models import IntervalSchedule, PeriodicTask


def update_cleanup_old_activity_logs_task(execution_interval_days: int) -> bool:
    try:
        schedule, _ = IntervalSchedule.objects.get_or_create(
            every=execution_interval_days, period=IntervalSchedule.DAYS
        )

        PeriodicTask.objects.update_or_create(
            name="cleanup_old_activity_logs",
            defaults={
                "interval": schedule,
                "task": "activity_logs.tasks.cleanup_old_activity_logs",
                "args": json.dumps([execution_interval_days]),
                "enabled": True,
            },
        )

        return True
    except Exception as e:
        print(f"[Celery Scheduler Control Error] {e}")
        return False


def delete_cleanup_task():
    try:
        deleted_count, _ = PeriodicTask.objects.filter(name="cleanup_old_activity_logs").delete()
        print(f"Deleted {deleted_count} periodic tasks named 'Cleanup old logs every day'.")
        return True
    except Exception as e:
        print(f"[Celery Scheduler Control Error] {e}")
        return False
