#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from ibiza_comunidad.users.models import UserProfile

def common_variables(request):

    return {
        'google_api': settings.GOOGLE_API_KEY,
    }

def user_profile_complete(request):
    incomplete = None
    if request.user.is_authenticated():
        if hasattr(request, 'user'):
            user = request.user
        else:
            user = None

        if user:
            if getattr(user, 'user_profile', None):
                incomplete = user.user_profile.is_incomplete()

    return {
        'is_user_profile_incomplete': incomplete,
    }

def has_profile(request):
    has_user_profile = False
    if request.user.is_authenticated():
        if not getattr(request.user, 'user_profile', None):
            # User has no profile
            # Create it
            UserProfile.objects.create(user=request.user)
            # Send message about it
            messages.success(request, _("We have upgraded your user account"))
        has_user_profile = True
    return {
        'has_profile': has_user_profile
    }
