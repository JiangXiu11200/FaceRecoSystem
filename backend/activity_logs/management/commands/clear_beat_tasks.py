from django.core.management.base import BaseCommand
from django_celery_beat.models import CrontabSchedule, IntervalSchedule, PeriodicTask


class Command(BaseCommand):
    help = "Delete all Celery Beat periodic tasks and their schedules."

    def handle(self, *args, **kwargs):
        PeriodicTask.objects.all().delete()
        IntervalSchedule.objects.all().delete()
        CrontabSchedule.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("All periodic tasks and schedules deleted."))
