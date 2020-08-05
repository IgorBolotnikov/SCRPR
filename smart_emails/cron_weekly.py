from datetime import datetime

from .suggestions import Suggestion


def send_suggestions():
    if datetime.today().weekday() == 0:
        return Suggestion(7).send_suggestions()
