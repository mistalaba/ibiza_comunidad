#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.utils.translation import ugettext_lazy as _

from allauth.account.models import EmailAddress

from .models import User
from .forms import ProfileForm_v2, UserForm

import logging
logger = logging.getLogger(__name__)


@login_required
def list_users(request):
    users = User.objects.all()
    return render(request, 'list_users.html', {
        'users': users,
    })


@login_required
def private_user_profile(request):
    user = request.user
    email = user.emailaddress_set.get_primary(user).email
    email_verified = user.emailaddress_set.get_primary(user).verified
    if request.method == 'POST':
        profile_form = ProfileForm_v2(request.POST, request.FILES, instance=user.profile)
        user_form = UserForm(request.POST, request.FILES, instance=user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, _("Your user profile is updated"))
            return redirect('users:private-profile')
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm_v2(instance=user.profile)
    return render(request, 'profile/private_profile.html', {
        'user': request.user,
        'user_form': user_form,
        'profile_form': profile_form,
        'email': email,
        'email_verified': email_verified,
    })


@login_required
def public_user_profile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'profile/public_profile.html', {
        'user': user,
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
