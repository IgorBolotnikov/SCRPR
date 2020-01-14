from celery.decorators import task
from celery.utils.log import get_task_logger
from django.template import loader


logger = get_task_logger(__name__)


@task(name='send_reset_password_email')
def send_reset_password_email(subject_template_name, email_template_name,
              context, from_email, to_email, html_email_template_name):

    subject = loader.render_to_string(subject_template_name, context)
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(email_template_name, context)

    email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, 'text/html')
    email_message.send()
