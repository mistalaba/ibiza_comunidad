#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from django.forms import widgets
from django.utils import timezone

from .models import Event

class EventForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(EventForm, self).__init__(*args, **kwargs)

    event_name = forms.CharField(max_length=400, required=True)
    photo = forms.ImageField(max_length=100, required=True)
    description = forms.CharField(max_length=600, required=False, widget=forms.Textarea)
    start = forms.DateTimeField(widget=widgets.DateTimeInput(attrs={'class': '_datetimepicker'}), required=True)
    end = forms.DateTimeField(widget=widgets.DateTimeInput(attrs={'class': '_datetimepicker'}), required=True)
    price = forms.DecimalField(widget=widgets.NumberInput(attrs={'step': 0.50}), max_digits=10, decimal_places=2, required=True)
    source = forms.URLField(required=False)
    location = forms.CharField(max_length=255, required=True)
    location_gmaps_place_id = forms.CharField(widget=forms.HiddenInput(), max_length=255, required=True)

class EventForm2(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(EventForm2, self).__init__(*args, **kwargs)

    class Meta:
        model = Event
        fields = [
            'title', 'photo', 'description',
            'start_datetime', 'end_datetime',
            'price', 'location_gmaps_place_id',
            'location_friendly_name'
        ]
        widgets = {
            'description': forms.Textarea,
            'start_datetime': widgets.DateTimeInput(attrs={'class': '_datetimepicker'}),
            'end_datetime': widgets.DateTimeInput(attrs={'class': '_datetimepicker'}),
            'location_gmaps_place_id': forms.HiddenInput,
        }
