from datetime import datetime

from .suggestions import Suggestion


def send_suggestions():
    if datetime.today().day == 1:
        return Suggestion(30).send_suggestions()
