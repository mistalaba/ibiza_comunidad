#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .forms import EventForm, EventForm2
from .models import Event

import logging
logger = logging.getLogger(__name__)


def list_events(request):
    events = Event.objects.all().order_by('-start_datetime')

    return render(request, 'list_events.html', {
        'events': events,
        'now': timezone.now(),
    })


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            data = form.cleaned_data
            event = Event.objects.create(
                title=data['event_name'],
                photo=data['photo'],
                description=data['description'],
                start_datetime=data['start'],
                end_datetime=data['end'],
                price=data['price'],
                created_by=request.user,
                location_friendly_name=data['location'],
                location_gmaps_place_id=data['location_gmaps_place_id'],
            )

            return redirect('events:list-events')
    else:
        form = EventForm(user=request.user)

    return render(request, 'create_event.html', {
        'form': form,
    })

@login_required
def edit_event(request, event_slug):
    event = get_object_or_404(Event, created_by=request.user, slug=event_slug)
    if request.method == 'POST':
        form = EventForm2(request.POST, request.FILES, user=request.user, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, _("Event successfully updated."))
            return redirect('events:list-events')
    else:
        form = EventForm2(user=request.user, instance=event)

    return render(request, 'edit_event.html', {
        'event': event,
        'form': form,
    })


@login_required
def event_detail(request, event_slug):
    event = Event.objects.get(slug=event_slug)

    return render(request, 'view_event.html', {
        'event': event,
    })


@login_required
def event_delete(request, event_slug):
    event = Event.objects.get(slug=event_slug)
    if event.created_by == request.user:
        event.delete()
        messages.success(request, _("Event successfully deleted."))
    else:
        messages.error(request, _("You cannot delete another user's event ."))

    return redirect('events:list-events')
