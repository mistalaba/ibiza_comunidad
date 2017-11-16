#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from django.utils import timezone

class EventForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(EventForm, self).__init__(*args, **kwargs)

    event_name = forms.CharField(max_length=400, required=True)
    photo = forms.ImageField(max_length=100, required=True)
    description = forms.CharField(max_length=600, required=False, widget=forms.Textarea)
    start = forms.DateTimeField(required=True)
    end = forms.DateTimeField(required=True)
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=True)
