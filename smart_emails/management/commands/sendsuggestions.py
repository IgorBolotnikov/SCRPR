from django.core.management.base import BaseCommand, CommandError
from smart_emails.suggestions import *


class Command(BaseCommand):
    '''send email suggestions to users based on favorites'''
    def handle(self, *args, **kwargs):
        Suggestion(1).send_suggestions()
