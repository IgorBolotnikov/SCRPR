from django.core.management.base import BaseCommand

from smart_emails.suggestions import Suggestion


class Command(BaseCommand):
    """
    Send daily email suggestions to users based on favorites.
    """

    def handle(self, *args, **kwargs):
        Suggestion(1).send_suggestions()
