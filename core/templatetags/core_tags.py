#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import template
from django.contrib.staticfiles import finders
from django.utils.html import mark_safe

register = template.Library()

@register.simple_tag
def include_svg(file_name):
    full_path = finders.find('images/' + file_name)
    return mark_safe(open(full_path).read())

# Get initials or avatar
@register.inclusion_tag('_avatar.html')
def avatar(user, size):
    # size: small (48x48), medium, large
    sizes = {'small': '48', 'medium': '64'}
    return {'user': user, 'size': sizes[size]}
