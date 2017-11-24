#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.utils.translation import ugettext_lazy as _

from allauth.account.models import EmailAddress

from .models import User
from .forms import ProfileForm

import logging
logger = logging.getLogger(__name__)


@login_required
def private_user_profile(request):
    User = get_user_model()
    user = request.user
    email = user.emailaddress_set.get_primary(user).email
    email_verified = user.emailaddress_set.get_primary(user).verified
    if request.method == 'POST':
        form = ProfileForm(request.POST, user=user)
        if form.is_valid():
            form.save(request)
            messages.success(request, _("Your user profile is updated"))
    else:
        data = {
            'username': user.username,
            'email': email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        form = ProfileForm(data, user=user)
    return render(request, 'profile/private_profile.html', {
        'user': request.user,
        'form': form,
        'email': email,
        'email_verified': email_verified,
    })


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['name', ]

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'
