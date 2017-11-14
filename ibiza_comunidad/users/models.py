from django.contrib.auth.models import AbstractUser
from django.core.signals import request_finished
from django.core.urlresolvers import reverse
from django.db import models
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from allauth.account.signals import email_confirmed, email_changed

import logging
logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

@receiver(email_confirmed)
def user_email_confirmed(request, email_address, **kwargs):
    # import ipdb; ipdb.set_trace()
    logger.info("Email is confirmed")
    # Change user's login email
    email_address.user.email = email_address.email
    email_address.user.save()

@receiver(email_changed)
def user_email_changed(request, user, from_email_address, to_email_address, **kwargs):
    logger.info("Email is changed")
