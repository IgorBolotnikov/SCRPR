from datetime import datetime
from smart_emails.suggestions import *


def send_suggestions():
    if datetime.today().weekday() == 0:
        return Suggestion(7).send_suggestions()
