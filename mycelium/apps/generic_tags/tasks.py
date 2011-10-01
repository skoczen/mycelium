from celery.task import task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

@task
def create_tag_group(tag):
    tag.create_tag_group_if_needed()