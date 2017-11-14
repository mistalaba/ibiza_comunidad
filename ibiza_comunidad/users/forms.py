#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from allauth.account.models import EmailAddress

import logging
logger = logging.getLogger(__name__)


class ProfileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ProfileForm, self).__init__(*args, **kwargs)

    username = forms.CharField()
    email = forms.EmailField()

    def clean_email(self):
        User = get_user_model()
        data = self.cleaned_data['email']
        # Check if new_email exists, both in user.email and EmailAddress
        user_email_exists = User.objects.filter(email__iexact=data).exclude(pk=self.user.pk).exists()
        email_address_exists = EmailAddress.objects.filter(email__iexact=data).exclude(user=self.user).exists()
        if user_email_exists or email_address_exists:
            self.add_error('email', ValidationError(_("The email {} already exists.").format(data)))
        return data

    def clean_username(self):
        User = get_user_model()
        data = self.cleaned_data['username']
        if User.objects.filter(username__iexact=data).exclude(pk=self.user.pk).exists():
            self.add_error('username', ValidationError(_("The username {} already exists.").format(data)))
        return data
