#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail import get_thumbnail

from .forms import EventForm, EventForm2
from .models import Event

import logging
logger = logging.getLogger(__name__)


def list_events(request):
    events = Event.objects.all().order_by('-start_datetime')

    # Today's events
    today = timezone.now().date()
    events_today = Event.objects.filter(start_datetime__date=today)
    excluded_events = events_today.values_list('pk', flat=True)
    print(excluded_events)

    # Tomorrow's events
    tomorrow = today + timezone.timedelta(days=1)
    events_tomorrow = Event.objects.filter(start_datetime__date=tomorrow).exclude(pk__in=excluded_events)
    excluded_events = excluded_events | events_tomorrow.values_list('pk', flat=True)
    print(excluded_events)

    # This month's events
    events_this_month = Event.objects.filter(end_datetime__gte=today, start_datetime__year=today.year, start_datetime__month=today.month).exclude(pk__in=excluded_events)
    excluded_events = excluded_events | events_this_month.values_list('pk', flat=True)

    # The rest
    all_other_events = Event.objects.exclude(pk__in=excluded_events)

    return render(request, 'list_events.html', {
        'events': events,
        'events_today': events_today,
        'events_tomorrow': events_tomorrow,
        'events_this_month': events_this_month,
        'all_other_events': all_other_events,
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
                source=data['source'],
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


def event_detail(request, event_slug):
    event = Event.objects.get(slug=event_slug)
    if request.is_ajax():
        photo = get_thumbnail(event.photo, '1024', quality=85)
        response = {
            'canonical_url': event.get_absolute_url(),
            'photo': photo.url,
            'title': event.title,
            'description': event.description,
            'start_datetime': event.start_datetime,
            'end_datetime': event.end_datetime,
            'price': event.price,
            'source': event.source,
            'location_friendly_name': event.location_friendly_name,
            'location_gmaps_place_id': event.location_gmaps_place_id,
            'created_by': {
                'username': event.created_by.username,
                'avatar': event.created_by.profile.avatar.url,
            }
        }
        return JsonResponse(response, safe=False)
    else:
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
