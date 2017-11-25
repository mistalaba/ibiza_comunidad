# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from ibiza_comunidad.taskapp.celery import app
from django.conf import settings
from django.core.mail import get_connection


import logging
logger = logging.getLogger(__name__)


@shared_task
def add(x, y):
    logger.info("Logging 'add'")
    return x + y


@app.task()
def add_number_two(x, y):
    logger.info("Logging 'add_number_two'")
    return x + y


@app.task()
def async_send_messages(email_messages):
    conn = get_connection(backend='anymail.backends.mailgun.EmailBackend')
    conn.send_messages(email_messages)
