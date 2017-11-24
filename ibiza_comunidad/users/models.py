#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import AbstractUser
from django.core.signals import request_finished
from django.core.urlresolvers import reverse
from django.db import models
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from allauth.account.signals import email_confirmed, email_changed, user_signed_up

import logging
logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    first_name = models.CharField(_('first name'), max_length=100, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

@receiver(email_confirmed)
def user_email_confirmed(request, email_address, **kwargs):
    logger.info("Email is confirmed")
    # Change user's login email
    email_address.user.email = email_address.email
    email_address.user.save()

@receiver(email_changed)
def user_email_changed(request, user, from_email_address, to_email_address, **kwargs):
    logger.info("Email is changed")

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    def is_incomplete(self):
        incomplete_fields = [self.user.first_name, self.user.last_name, self.user.email]
        for field in incomplete_fields:
            if not field:
                logger.info("Profile is incomplete: {}".format(field))
                return True
            else:
                logger.info("Field value: {}".format(field))
        return False

@receiver(user_signed_up)
def create_profile(sender, **kwargs):
    request = kwargs['request']
    user = kwargs['user']
    UserProfile.objects.create(user=user)
    user.save()
