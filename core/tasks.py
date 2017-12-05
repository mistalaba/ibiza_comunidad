# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from ibiza_comunidad.taskapp.celery import app
from django.conf import settings
from django.core.mail import get_connection

from .utils import remove_unsubscribe


import logging
logger = logging.getLogger(__name__)


@app.task()
def async_send_messages(email_messages):
    conn = get_connection(backend='anymail.backends.mailgun.EmailBackend')
    conn.send_messages(email_messages)

@app.task()
def async_remove_unsubscribe(email, tag):
    remove_unsubscribe(email, tag)
