#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation

from sorl.thumbnail import ImageField as SorlImageField
from sorl.thumbnail import get_thumbnail
from taggit.managers import TaggableManager

from core.models import TimeStampedModel, Comment
from core.utils import slugify_unique


class Event(TimeStampedModel):
    class Meta:
        ordering = ['start_datetime']
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
    comments = GenericRelation(Comment)
    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse('events:event-detail', kwargs={'event_slug': self.slug})

    def algolia_photo_url(self):
        return self.photo.url if self.photo else ''

    def algolia_photo_url_medium(self):
        photo = get_thumbnail(self.photo, '1024', quality=85) if self.photo else ''
        if photo:
            return photo.url
        return ''


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_unique(self, 'title', max_length=50)
        super().save()
