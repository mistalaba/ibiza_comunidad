#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings


class Event(models.Model):
    title = models.CharField(max_length=400)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
