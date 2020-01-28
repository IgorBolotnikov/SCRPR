from celery.decorators import task
from celery.utils.log import get_task_logger
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.template import loader
from django.conf import settings
from authentication.models import User


logger = get_task_logger(__name__)


@task(name='send_reset_password_email')
def send_reset_password_email(subject_template_name, email_template_name,
              context, from_email, to_email, html_email_template_name):

    context['user'] = User.objects.get(pk=context['user'])
    subject = loader.render_to_string(subject_template_name, context)
    subject = ''.join(subject.splitlines())
    html_email = loader.render_to_string(html_email_template_name, context)

    if settings.DEBUG:
        print(context)
    else:
        message = Mail(
            from_email='bolotnikovprojects@gmail.com',
            to_emails=to_email,
            subject=subject,
            html_content=html_with_context,
        )
        sg_client = SendGridAPIClient(settings.EMAIL_HOST_PASSWORD)
        response = sg_client.send(message)
