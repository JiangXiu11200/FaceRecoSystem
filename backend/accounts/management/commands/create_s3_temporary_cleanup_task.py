from django.core.management.base import BaseCommand

from accounts.utils.celery_scheduler_control import update_s3_temporary_file_cleanup_task


class Command(BaseCommand):
    help = "Create periodic task for cleaning up S3 temporary data"

    def handle(self, *args, **kwargs):
        created = update_s3_temporary_file_cleanup_task(run_at_startup=True)
        if created:
            self.stdout.write(self.style.SUCCESS("Periodic task 'cleanup_s3_temporary_data' created successfully."))
        else:
            self.stdout.write(self.style.WARNING("Failed to create periodic task 'cleanup_s3_temporary_data'."))
