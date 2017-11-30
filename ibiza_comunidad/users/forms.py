#!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image

from django import forms
from django.core import validators
from django.core.files import File
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from allauth.account.models import EmailAddress

from core.validators import validate_unicode_username
from ibiza_comunidad.users.models import User, UserProfile

import logging
logger = logging.getLogger(__name__)

class ProfileForm_v2(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = UserProfile
        fields = ['avatar', 'x', 'y', 'width', 'height']

    def save(self):
        profile = super(ProfileForm_v2, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(profile.avatar)
        cropped_image = image.crop((x, y, w+x, h+y))
        if cropped_image.width > 1024:
            resized_image = cropped_image.resize((1024, 1024), Image.ANTIALIAS)
            resized_image.save(profile.avatar.path)
        else:
            cropped_image.save(profile.avatar.path, format='JPEG', quality=85)

        return profile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
