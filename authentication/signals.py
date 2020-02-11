from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created

from authentication.tasks import send_reset_password_email


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token,
                                 *args, **kwargs):
    # send an e-mail to the user
    context = {
        'user': reset_password_token.user.id,
        'reset_password_url': "{}?token={}".format(
            reverse('password_reset:reset-password-request'),
            reset_password_token.key
        )
    }
    send_reset_password_email.delay(
        subject_template_name='authentication/reset_password_subject.txt',
        email_template_name='authentication/reset_password_message.html',
        context=context,
        from_email='bolotnikovprojects@gmail.com',
        to_email=reset_password_token.user.email,
        html_email_template_name='authentication/reset_password_message.html'
    )
