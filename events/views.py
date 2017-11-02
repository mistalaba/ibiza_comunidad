#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect

from .forms import EventForm
from .models import Event

def list_events(request):
    events = Event.objects.all()

    return render(request, 'list_events.html', {
        'events': events,
    })


def create_event(request):
    form = EventForm(request.POST or None, user=request.user)

    if form.is_valid():
        data = form.cleaned_data
        event = Event.objects.create(title=data['title'], created_by=request.user)

        return redirect('events:list-events')


    return render(request, 'create_event.html', {
        'form': form,
    })

