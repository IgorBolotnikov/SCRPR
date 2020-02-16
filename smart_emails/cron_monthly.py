from datetime import datetime
from smart_emails.suggestions import *


def send_suggestions():
    if datetime.today().day == 1:
        return Suggestion(30).send_suggestions()
