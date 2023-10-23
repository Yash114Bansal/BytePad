from django.core.management.base import BaseCommand
from accounts.models import Course
from .courses import courses


class Command(BaseCommand):
    help = "Create courses from a dictionary"

    def handle(self, *args, **options):
        for branch, semesters in courses.items():
            for semester, course_list in semesters.items():
                for course_info in course_list:
                    course_code = course_info["Course Code"]
                    course_name = course_info["Course Name"]
                    Course.objects.create(
                        name=course_name,
                        branch=branch,
                        semester=int(semester.strip("Semester ")),
                        course_code=course_code,
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f"Created course: {course_code}")
                    )
