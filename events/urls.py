#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.list_events, name='list-events'),
    url(r'^create/$', views.create_event, name='create-event'),
]
