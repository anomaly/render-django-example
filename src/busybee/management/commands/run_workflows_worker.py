"""
Django wrapper for render workflow

"""

from django.conf import settings
from django.core.management.base import BaseCommand

app = settings.WORKFLOW_APP


class Command(BaseCommand):
    def handle(self, *args, **options):
        app.start()
