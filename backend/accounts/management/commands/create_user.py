from django.core.management.base import BaseCommand

from accounts.models import SystemApps, UserGroup, UserProfile
from accounts.utils.verify_passward import make_hashed_password


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Create a default user group if it doesn't exist
        default_group, created = UserGroup.objects.get_or_create(defaults={"group_name": "Administrator"}, id=1)

        # Get all system apps
        system_apps = SystemApps.objects.all()
        if created:
            # Add all system apps to the default group
            default_group.apps.add(*system_apps)
            self.stdout.write(self.style.SUCCESS("Created default user group and added all system apps"))

        if created:
            self.stdout.write(self.style.SUCCESS("Created default user group: Default Group"))
        else:
            self.stdout.write(self.style.WARNING("Default user group already exists."))

        # Add default system apps to the default group
        system_apps = SystemApps.objects.all()
        for app in system_apps:
            if not default_group.apps.filter(id=app.id).exists():
                default_group.apps.add(app)
                self.stdout.write(self.style.SUCCESS(f"Added app '{app.app_name}' to default group."))

        # Create superadmin user
        _password = make_hashed_password("superadmin")
        default_user, created = UserProfile.objects.get_or_create(
            defaults={
                "account": "superadmin",
                "password": _password,
                "first_name": "superadmin",
            }
        )
        if created:
            default_user.user_groups.add(default_group)
            default_user.save()
            self.stdout.write(self.style.SUCCESS("Created default user: superadmin"))
        else:
            self.stdout.write(self.style.WARNING("Default user 'superadmin' already exists."))
