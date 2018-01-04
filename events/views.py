#!/usr/bin/python
# -*- coding: utf-8 -*-
import calendar
import datetime
from dateutil.relativedelta import relativedelta

from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail import get_thumbnail

from ibiza_comunidad.users.utils import get_initials
from .forms import EventForm, EventForm2, CommentForm
from .models import Event

import logging
logger = logging.getLogger(__name__)


def list_events(request):
    events = Event.objects.all().order_by('-start_datetime')

    # Today's events
    today = timezone.now().date()
    now = timezone.now()
    q_today = Q(start_datetime__date=today) & Q(end_datetime__gt=now)
    events_today = Event.objects.filter(q_today)

    # Tomorrow's events
    tomorrow = today + timezone.timedelta(days=1)
    q_tomorrow = Q(start_datetime__date=tomorrow)
    events_tomorrow = Event.objects.filter(q_tomorrow)

    # This month's events
    end_of_month = datetime.date(today.year, today.month, calendar.monthrange(today.year, today.month)[1])
    q_this_month = Q(start_datetime__date__gt=tomorrow) & Q(start_datetime__date__lte=end_of_month)
    events_this_month = Event.objects.filter(q_this_month)

    # The rest
    next_month = today.replace(day=1) + relativedelta(months=1)
    q_rest = Q(start_datetime__gte=next_month)
    all_other_events = Event.objects.filter(q_rest)

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
        comments = []
        for comment in event.comments.all():
            if comment.created_by.profile.avatar:
                avatar_url = get_thumbnail(comment.created_by.profile.avatar, '48', quality=85).url
            else:
                avatar_url = ''
            current_comment = {
                'comment': comment.comment,
                'created': comment.created,
                'created_by': {
                    'username': comment.created_by.username,
                    'avatar_url': avatar_url,
                    'color': comment.created_by.profile.color,
                    'initials': get_initials(comment.created_by),
                },

            }
            comments.append(current_comment)

        response = {
            'type': 'event',
            'id': event.pk,
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
                'avatar_url': get_thumbnail(event.created_by.profile.avatar, '48', quality=85).url if event.created_by.profile.avatar else '',
                'color': event.created_by.profile.color,
                'initials': get_initials(event.created_by),
            },
            'comments': comments,
            'tags': [tag.name for tag in event.tags.all()],
        }
        return JsonResponse(response, safe=False)
    else:
        commentform = CommentForm(request.POST or None, user=request.user, event=event)
        if request.method == 'POST':
            if commentform.is_valid():
                commentform.save()
                return redirect('events:event-detail', event_slug=event_slug)
        return render(request, 'view_event.html', {
            'event': event,
            'commentform': commentform,
            'comments': event.comments.all()
        })


@login_required
def save_ajax_comment(request):
    if request.method == 'POST':
        # Get event
        event_id = request.POST.get('event')
        event = Event.objects.get(pk=event_id)
        comment = request.POST.get('comment')
        # Create comment
        comment_created = event.comments.create(comment=comment, created_by=request.user)

        if comment_created.created_by.profile.avatar:
            avatar_url = get_thumbnail(comment_created.created_by.profile.avatar, '48', quality=85).url
        else:
            avatar_url = ''

        current_comment = {
            'id': comment_created.pk,
            'comment': comment_created.comment,
            'created': comment_created.created,
            'created_by': {
                'username': comment_created.created_by.username,
                'avatar_url': avatar_url,
                'color': comment_created.created_by.profile.color,
                'initials': get_initials(comment_created.created_by),
            },
        }

    response = current_comment
    return JsonResponse(response, safe=False)

@login_required
def event_delete(request, event_slug):
    event = Event.objects.get(slug=event_slug)
    if event.created_by == request.user:
        event.delete()
        messages.success(request, _("Event successfully deleted."))
    else:
        messages.error(request, _("You cannot delete another user's event ."))

    return redirect('events:list-events')
