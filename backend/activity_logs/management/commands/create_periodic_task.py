from django.core.management.base import BaseCommand

from activity_logs.utils.celery_scheduler_control import update_cleanup_old_activity_logs_task


class Command(BaseCommand):
    help = "Create periodic task for cleanup_old_activity_logs"

    def handle(self, *args, **kwargs):
        created = update_cleanup_old_activity_logs_task(execution_interval_days=90)
        if created:
            self.stdout.write(self.style.SUCCESS("Periodic task 'cleanup_old_activity_logs' created successfully."))
        else:
            self.stdout.write(self.style.WARNING("Failed to create periodic task 'cleanup_old_activity_logs'."))
