#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from django.utils import timezone

class EventForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(EventForm, self).__init__(*args, **kwargs)

    title = forms.CharField(max_length=400, required=True)
