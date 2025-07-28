from django.core.management.base import BaseCommand

from accounts.models import SystemApps


class Command(BaseCommand):
    def handle(self, *args, **options):
        _, created = SystemApps.objects.update_or_create(defaults={"app_name": "accounts", "label": "Accounts"}, id=1)
        if created:
            self.stdout.write(self.style.SUCCESS("Created default app: Accounts"))
        else:
            self.stdout.write(self.style.WARNING("Default app 'Accounts' already exists."))
