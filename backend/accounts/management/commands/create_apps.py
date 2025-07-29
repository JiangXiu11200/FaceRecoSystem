from django.core.management.base import BaseCommand

from accounts.models import SystemApps


class Command(BaseCommand):
    def handle(self, *args, **options):
        apps = [
            {"id": 1, "app_name": "accounts", "label": "Accounts"},
            {"id": 2, "app_name": "facerecognition", "label": "Face Recognition"},
            {"id": 3, "app_name": "userregistration", "label": "User Registration"},
            {"id": 4, "app_name": "alarmlogs", "label": "Alarm Logs"},
            {"id": 5, "app_name": "activitylogs", "label": "Activity Logs"},
            {"id": 6, "app_name": "facerecognitionconfig", "label": "Face Recognition Config"},
        ]

        for app in apps:
            _, created = SystemApps.objects.update_or_create(
                id=app["id"], defaults={"app_name": app["app_name"], "label": app["label"]}
            )

            status = "Created" if created else "Already exists"
            self.stdout.write(
                self.style.SUCCESS(f"{status}: {app['label']} (ID: {app['id']})")
                if created
                else self.style.WARNING(f"{status}: {app['label']} (ID: {app['id']})")
            )
