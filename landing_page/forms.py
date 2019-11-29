from django import forms
from django.core.mail import send_mail
from os import environ

MESSAGE_SUBJECT = 'Message from your Webpage'
EMAIL_ATTRS = {
    'class': 'field',
    'placeholder': 'Email',
}
SENDER_ATTRS = {
    'class': 'field',
    'placeholder': 'Name',
}
SUBJECT_ATTRS = {
    'class': 'field',
    'placeholder': 'Subject'
}
MESSAGE_ATTRS = {
    'class': 'field',
    'rows': 8,
    'cols': 80,
    'placeholder': 'Message',
}

class ContactForm(forms.Form):
    email = forms.EmailField(
        max_length=100,
        widget=forms.TextInput(attrs=EMAIL_ATTRS))
    sender = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs=SENDER_ATTRS))
    subject = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs=SUBJECT_ATTRS))
    body = forms.CharField(widget=forms.Textarea(attrs=MESSAGE_ATTRS))

    @staticmethod
    def _make_message(name, email, subject, message_body):
        message_header = f'From: {name}, email: <{email}>\nSubject: {subject}\n\n'
        return message_header + message_body

    def send_message(self, name, email, subject, message_body):
        message = self._make_message(name, email, subject, message_body)
        send_mail(
            MESSAGE_SUBJECT,
            message,
            environ.get('MAIL_USERNAME'),
            [environ.get('OWN_EMAIL')]
        )
