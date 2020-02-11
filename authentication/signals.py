from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created

from authentication.tasks import send_reset_password_email


RESET_PASSWORD_URL = settings.FRONTEND_URL + '/auth/reset-password/'


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token,
                                 *args, **kwargs):
    # send an e-mail to the user
    context = {
        'user': reset_password_token.user.id,
        'reset_password_url': "{}{}".format(
            RESET_PASSWORD_URL,
            reset_password_token.key
        )
    }
    send_reset_password_email(
        subject_template_name='authentication/reset_password_subject.txt',
        email_template_name='authentication/reset_password_message.html',
        context=context,
        from_email='bolotnikovprojects@gmail.com',
        to_email=reset_password_token.user.email,
        html_email_template_name='authentication/reset_password_message.html'
    )
