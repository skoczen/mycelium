from celery.task import task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

@task
def send_welcome_emails(account, useraccount):

    # Send them a welcome email
    send_mail("Welcome to GoodCloud!", "%s" % render_to_string("accounts/welcome_email.txt", locals()), settings.SERVER_EMAIL, [useraccount.email] )

    # Send us a notification that we have a new signup!
    send_mail("New Account: %s!" % (account,), "%s" % render_to_string("accounts/new_signup_email.txt", locals()), settings.SERVER_EMAIL, settings.MANAGERS )    