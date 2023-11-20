from django.core.management.base import BaseCommand
from timetable.models import LectureNumberModel
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Create LectureNumberModel instances'

    def handle(self, *args, **kwargs):
        start_time = datetime.strptime('08:30', '%H:%M')
        end_time = datetime.strptime('09:20', '%H:%M')
        lecture_duration = timedelta(minutes=50)

        for i in range(1, 10):
            lecture_start = start_time + (i - 1) * lecture_duration
            lecture_end = lecture_start + lecture_duration

            # Create LectureNumberModel
            lecture_number, created = LectureNumberModel.objects.get_or_create(
                slot=i,
                start_time=lecture_start.time(),
                end_time=lecture_end.time()
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Lecture Number {i} created successfully.'))

        self.stdout.write(self.style.SUCCESS('Lectures created successfully.'))
