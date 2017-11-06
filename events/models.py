#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings

from core.models import TimeStampedModel


class Event(TimeStampedModel):
    title = models.CharField(max_length=400)
    photo = models.ImageField(upload_to='event_photos/', max_length=100, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
