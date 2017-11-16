#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.list_events, name='list-events'),
    url(r'^(?P<event_slug>[A-Za-z0-9\-\_]+)/$', views.event_detail, name='event-detail'),
    url(r'^create/$', views.create_event, name='create-event'),
]
