from django.core.management.base import BaseCommand
from accounts.models import Semester
from .config import semesters


class Command(BaseCommand):
    help = "Create courses from a List"

    def handle(self, *args, **options):
        for semester in semesters:
            Semester.objects.create(name=semester[1],semester = semester[0])

            self.stdout.write(
                        self.style.SUCCESS(f"Created Semester: {semester[1]}")
                    )