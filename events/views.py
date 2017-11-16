#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import EventForm
from .models import Event

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
                created_by=request.user)

            return redirect('events:list-events')
    else:
        form = EventForm(user=request.user)


    return render(request, 'create_event.html', {
        'form': form,
    })


def event_detail(request, event_slug):
    event = Event.objects.get(slug=event_slug)

    return render(request, 'view_event.html', {
        'event': event,
    })
