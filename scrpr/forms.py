from os import environ
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.forms import (
    Form,
    ModelForm,
    CharField,
    BooleanField,
    ChoiceField,
    IntegerField,
    DecimalField,
    EmailField,
    EmailInput,
    TextInput,
    PasswordInput,
    NumberInput,
    Textarea,
    CheckboxInput,
    Select,
    FileInput
)
from django.conf import settings
from django.core.mail import send_mail
from .models import Comment, FavoriteGameQuery, FavoriteJobQuery
from .constants import *
from authentication.models import User


class RateForm(ModelForm):
    error_css_class = 'rate_error'

    class Meta:
        model = Comment
        fields = ['name', 'comment']
        widgets = {
            'name': TextInput(attrs=RATE_NAME_ATTRS),
            'comment': Textarea(attrs=RATE_COMMENT_ATTRS)
        }

    @staticmethod
    def _make_message(name, message_body):
        message_header = f'From {name}\n\n'
        return message_header + message_body

    def send_message(self, name, message_body):
        message_body = self._make_message(name, message_body)
        message = Mail(
            settings.PROJECT_EMAIL,
            to_emails=settings.OWN_EMAIL,
            subject=MESSAGE_SUBJECT,
            html_content=message_body,
        )
        sg_client = SendGridAPIClient(settings.EMAIL_HOST_PASSWORD)
        try:
            response = sg_client.send(message)
        except Exception as exception:
            print(str(exception))


class GamesForm(ModelForm):
    class Meta:
        model = FavoriteGameQuery
        fields = [
            'title',
            'price_min',
            'price_max',
            'psplus_price',
            'initial_price',
            'free',
            'notification_freq',
            'account'
        ]
        widgets = {
            'title': TextInput(attrs=GAMES_INPUT_ATTRS),
            'price_min': NumberInput(attrs=NUMERIC_FILTER_ATTRS),
            'price_max': NumberInput(attrs=NUMERIC_FILTER_ATTRS),
            'psplus_price': CheckboxInput(attrs=CHECKBOX_ATTRS),
            'initial_price': CheckboxInput(attrs=CHECKBOX_ATTRS),
            'free': CheckboxInput(attrs=CHECKBOX_ATTRS),
            'notification_freq': Select(attrs=CITIES_ATTRS),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = GAMES_TITLE_LABEL
        self.fields['price_min'].label = NUMERIC_MIN_LABEL
        self.fields['price_max'].label = NUMERIC_MAX_LABEL
        self.fields['psplus_price'].label = PSPLUS_PRICE_LABEL
        self.fields['initial_price'].label = INITIAL_PRICE_LABEL
        self.fields['free'].label = FREE_LABEL
        self.fields['notification_freq'].label = NOTIFICATION_LABEL


class JobsForm(ModelForm):
    class Meta:
        model = FavoriteJobQuery
        fields = [
            'title',
            'city',
            'salary_min',
            'salary_max',
            'with_salary',
            'notification_freq',
            'account'
        ]
        widgets = {
            'title': TextInput(attrs=JOBS_INPUT_ATTRS),
            'city': Select(attrs=CITIES_ATTRS),
            'salary_min': NumberInput(attrs=NUMERIC_FILTER_ATTRS),
            'salary_max': NumberInput(attrs=NUMERIC_FILTER_ATTRS),
            'with_salary': CheckboxInput(attrs=CHECKBOX_ATTRS),
            'notification_freq': Select(attrs=CITIES_ATTRS),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = JOBS_TITLE_LABEL
        self.fields['salary_min'].label = NUMERIC_MIN_LABEL
        self.fields['salary_max'].label = NUMERIC_MAX_LABEL
        self.fields['with_salary'].label = WITH_SALARY_LABEL
        self.fields['notification_freq'].label = NOTIFICATION_LABEL
