from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.utils import timezone


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('create', type=str)

    def handle(self, *args, **kwargs):
        interval, _ = IntervalSchedule.objects.get_or_create(every=3, period='minutes')
        try:
            PeriodicTask.objects.create(
                name='Update locations car',
                task='api.tasks.update_locations_car',
                interval=interval,
                start_time=timezone.now(),
            )
        except ValidationError:
            self.stdout.write(self.style.SUCCESS('Update locations task already created'))
            return
        self.stdout.write(self.style.SUCCESS('Update locations task created successfully'))
