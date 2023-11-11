from django.core.management.base import BaseCommand
from accounts.models import Branch
from .config import branches


class Command(BaseCommand):
    help = "Create courses from a List"

    def handle(self, *args, **options):
        for branch in branches:
            Branch.objects.create(name=branch[0], full_name=branch[1])

            self.stdout.write(self.style.SUCCESS(f"Created Branch: {branch[1]}"))
