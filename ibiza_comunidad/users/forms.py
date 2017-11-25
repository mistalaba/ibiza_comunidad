#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from django.core import validators
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from allauth.account.models import EmailAddress

from core.validators import validate_unicode_username
from ibiza_comunidad.users.models import User, UserProfile

import logging
logger = logging.getLogger(__name__)

class ProfileForm_v2(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
