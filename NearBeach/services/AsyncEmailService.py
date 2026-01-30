from typing import List

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import threading, logging


class AsyncEmailService(threading.Thread):
    """Service to help send emails asynchronously"""

    def __init__(self, subject: str, template: str, recipient_list: List[str], context: dict) -> None:
        """Initialise the class"""
        self.subject = subject
        self.template = template
        self.recipient_list = recipient_list
        self.context = context
        threading.Thread.__init__(self)

    def run(self):
        try:
            """Send emails asynchronously"""
            html_content = render_to_string(
                template_name=self.template,
                context=self.context,
            )

            email = EmailMultiAlternatives(
                subject=self.subject,
                body=strip_tags(html_content),
                to=self.recipient_list,
            )

            email.attach_alternative(html_content, "text/html")
            email.send()
        except Exception as e:
            logging.error(e)
