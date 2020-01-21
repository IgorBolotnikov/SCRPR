from django.core.management.base import BaseCommand
from smart_emails.suggestions import *


class Command(BaseCommand):
    '''send email suggestions to users based on favorites'''
    def handle(self, *args, **kwargs):
        Suggestion(1).send_suggestions()
        Suggestion(7).send_suggestions()
        Suggestion(30).send_suggestions()
