#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from django.core import validators
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from allauth.account.models import EmailAddress

from core.validators import validate_unicode_username
import logging
logger = logging.getLogger(__name__)


class ProfileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ProfileForm, self).__init__(*args, **kwargs)

    # max_length taken from model
    username = forms.CharField(max_length=150, validators=[validate_unicode_username])
    email = forms.EmailField(max_length=254)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

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

    def save(self, request):
        data = self.cleaned_data
        user = self.user
        email = user.emailaddress_set.get_primary(user).email
        if data['email'] != email:
            # User changed email address
            new_email = data['email']
            email = EmailAddress.objects.get_primary(user)
            email.change(request, new_email=new_email)
        user.username = data['username']
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.save()


