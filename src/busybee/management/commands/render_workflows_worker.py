"""
Django wrapper for render workflow

"""

from django.core.management.base import BaseCommand
from render_sdk import Workflows


app = Workflows.from_workflows()


class Command(BaseCommand):
    """
    Runs render workflow worker with the ability to provide the
    Django context to the commands
    """

    def handle(self, *args, **options):
        app.start()
