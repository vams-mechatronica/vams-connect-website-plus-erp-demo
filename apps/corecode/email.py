import threading
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import logging
logger = logging.getLogger(__name__)
def send_html_email_async(subject, to_emails, content_context, template=None):
    """
    Sends an HTML email asynchronously using threading.

    :param subject: Email subject
    :param to_emails: List of recipient email addresses
    :param content_context: Context dictionary for rendering the HTML template
    :param template: Path to the HTML template (default is 'emails/base_template.html')
    """
    def send_email():

        try:
            if template:
                html_content = render_to_string(template, content_context)
            else:
                html_content = "<p>A form has been filled.</p>"
        except Exception as e:
            logger.exception("Failed to render email template.")
            html_content = "<p>A form has been filled.</p>"


        try:
            from_email = settings.DEFAULT_FROM_EMAIL
            msg = EmailMultiAlternatives(subject, '', from_email, to_emails)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except Exception as e:
            logger.exception("Failed to send email.")

    thread = threading.Thread(target=send_email)
    thread.start()
