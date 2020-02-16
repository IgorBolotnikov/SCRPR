from celery.decorators import task
from celery.utils.log import get_task_logger

import sendgrid

from django.template import loader
from django.conf import settings
from django.core.mail import send_mail

from authentication.models import User


logger = get_task_logger(__name__)


# @task(name='send_reset_password_email')
def send_reset_password_email(subject_template_name, email_template_name,
              context, from_email, to_email, html_email_template_name):

    context['user'] = User.objects.get(pk=context['user'])
    subject = loader.render_to_string(subject_template_name, context)
    subject = ''.join(subject.splitlines())
    html_email = loader.render_to_string(html_email_template_name, context)
    
    message = sendgrid.helpers.mail.Mail(
        from_email='bolotnikovprojects@gmail.com',
        to_emails=to_email,
        subject=subject,
        html_content=html_email,
    )
    sg_client = sendgrid.SendGridAPIClient(settings.EMAIL_HOST_PASSWORD)
    response = sg_client.send(message)
