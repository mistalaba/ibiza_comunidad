#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.validators import _lazy_re_compile, RegexValidator
from django.utils.translation import ugettext_lazy as _

slug_unicode_re = _lazy_re_compile(r'^[-\w]+\Z')
validate_unicode_username = RegexValidator(
    slug_unicode_re,
    _("Enter a valid username consisting of Unicode letters, numbers, underscores, or hyphens."),
    'invalid'
)
