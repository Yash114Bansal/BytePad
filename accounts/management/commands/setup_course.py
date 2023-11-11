from django.core.management.base import BaseCommand
from accounts.models import Course
from .config import courses


class Command(BaseCommand):
    help = "Create courses from a List"

    def handle(self, *args, **options):
        for course in courses:
            name = course["Course Name"]
            course_code = course["Course Code"]
            Course.objects.create(name=name ,course_code=course_code)

            self.stdout.write(
                        self.style.SUCCESS(f"Created Course: {name}")
                    )