from __future__ import absolute_import
from celery import Celery
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.template import loader
from django.core.mail import EmailMultiAlternatives

app = Celery('tasks', backend='amqp', broker='amqp://')


@app.task(ignore_result=True, name='tasks.send_reset_mail')
def send_reset_mail(email):
    from django.contrib.auth.models import User
    domain_override = None
    use_https = False
    template_name = 'reset.html'
    email_template_name = 'reset_email.html'
    subject_template_name='reset_subject.txt'
    for user in User.objects.filter(email__iexact=email, is_active=True):
        site_name = domain = 'dev.it-open.com:8037'
        context = {
            'email': user.email,
            'domain': domain,
            'site_name': site_name,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': token_generator.make_token(user),
            'protocol': 'https' if use_https else 'http',
        }
        send_mail(subject_template_name, email_template_name, context,
                  'TheHealth.me <noreply@thehealth.me>', user.email)


def send_mail(subject_template_name, email_template_name,
              context, from_email, to_email, html_email_template_name=None):
        """
        Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()