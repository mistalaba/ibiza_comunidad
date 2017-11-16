#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.utils.text import slugify

def slugify_unique(instance, field_to_slugify):
    """
    Idea taken from http://fazle.me/auto-generating-unique-slug-in-django/
    """
    model = instance._meta.model
    base_slug = slugify(getattr(instance, field_to_slugify))
    # Continue the slugification
    unique_slug = base_slug
    num = 1
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = '{}-{}'.format(slug, num)
        num += 1
    return unique_slug
