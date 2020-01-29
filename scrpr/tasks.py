from celery.decorators import task
from celery.utils.log import get_task_logger
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.template import loader
from django.conf import settings
from authentication.models import User


logger = get_task_logger(__name__)


@task(name='send_500_error_email')
def send_500_error_email(path):
    subject = '500 Error in SCRPR'
    html_email = loader.render_to_string(
        'scrpr/emails/500.html',
        {'path': path}
    )
    if settings.DEBUG:
        print(context)
    else:
        message = Mail(
            from_email='bolotnikovprojects@gmail.com',
            to_emails=settings.OWN_EMAIL,
            subject=subject,
            html_content=html_with_context,
        )
        sg_client = SendGridAPIClient(settings.EMAIL_HOST_PASSWORD)
        response = sg_client.send(message)
