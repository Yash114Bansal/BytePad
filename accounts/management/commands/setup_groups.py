from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = "Initialize Groups"

    def handle(self, *args, **options):
        department_head_group, created = Group.objects.get_or_create(name='Department Heads')
        faculty_group, created = Group.objects.get_or_create(name='Faculty')
        student_group, created = Group.objects.get_or_create(name='Students')
        self.stdout.write(self.style.SUCCESS('Groups set up successfully.'))