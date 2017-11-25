#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from ibiza_comunidad.users.models import UserProfile

class UpgradeUserProfileMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.is_authenticated():
            if not getattr(request.user, 'user_profile', None):
                # User has no profile
                # Create it
                UserProfile.objects.create(user=request.user)
                # Send message about it
                messages.success(request, _("We have upgraded your user account"))

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
