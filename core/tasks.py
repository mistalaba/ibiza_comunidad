# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from ibiza_comunidad.taskapp.celery import app

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

