from django.core.management.base import BaseCommand
from utils.minio_client import MinioClient


class Command(BaseCommand):
    def handle(self, *args, **options):
        buckets = ["accounts", "temporary-data", "user-registration", "face-activity-logs", "face-alarm-logs"]

        for bucket_name in buckets:
            try:
                status, message = MinioClient.create_bucket(bucket_name)
                if status:
                    self.stdout.write(self.style.SUCCESS(f"Bucket '{bucket_name}' created successfully."))
                else:
                    self.stderr.write(
                        self.style.WARNING(f"Bucket '{bucket_name}' already exists or could not be created: {message}")
                    )
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error creating bucket '{bucket_name}': {str(e)}"))
