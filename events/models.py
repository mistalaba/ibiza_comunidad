#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings

from sorl.thumbnail import ImageField as SorlImageField

from core.models import TimeStampedModel
from core.utils import slugify_unique


class Event(TimeStampedModel):
    title = models.CharField(max_length=400)
    photo = SorlImageField(upload_to='event_photos/', max_length=100, null=True)
    description = models.CharField(max_length=600, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    location_gmaps_place_id = models.CharField(max_length=255, blank=True)
    location_friendly_name = models.CharField(max_length=255, blank=True)
    slug = models.CharField(max_length=50, blank=True)
    source = models.URLField(blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_unique(self, 'title')
        super().save()
