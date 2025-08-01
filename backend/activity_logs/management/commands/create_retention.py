from django.core.management.base import BaseCommand

from activity_logs.models import FaceRecognitionActivityLogsRetention, SystemActivityLogsRetention


class Command(BaseCommand):
    help = "Create default retention settings for activity logs"

    def handle(self, *args, **kwargs):
        system_retention, created = SystemActivityLogsRetention.objects.update_or_create(
            defaults={"retention_days": 90}
        )
        self.stdout.write(f"{'Created' if created else 'Updated'} SystemActivityLogsRetention: {system_retention}")

        face_recognition_retention, created = FaceRecognitionActivityLogsRetention.objects.update_or_create(
            defaults={"retention_days": 90}
        )
        self.stdout.write(
            f"{'Created' if created else 'Updated'} FaceRecognitionActivityLogsRetention: {face_recognition_retention}"
        )
