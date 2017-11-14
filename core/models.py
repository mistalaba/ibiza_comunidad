#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models

class TimeStampedModel(models.Model):
    """ An abstract base class model that provides selfupdating ``created`` and ``modified`` fields. """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True