#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from django.forms import widgets
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from taggit.models import Tag

from core.models import Comment
from core.widgets import CategoryCheckboxSelectMultiple
from .models import Event


class EventForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        # self.tags = Tag.objects.all()
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
    categories = forms.MultipleChoiceField(widget=CategoryCheckboxSelectMultiple(attrs={'class': 'category'}), choices=[(tag.name, tag.name) for tag in Tag.objects.all()])


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


class CommentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.event = kwargs.pop('event')
        super(CommentForm, self).__init__(*args, **kwargs)

    comment = forms.CharField(max_length=600, required=False, widget=forms.Textarea(attrs={'placeholder': _('Write your comment here'), 'rows': '2'}))

    def save(self):
        data = self.cleaned_data
        self.event.comments.create(comment=data['comment'], created_by=self.user)


class EventSearchForm(forms.Form):
    q = forms.CharField(max_length=100, required=False, label='Event')
    categories = forms.MultipleChoiceField(widget=CategoryCheckboxSelectMultiple(attrs={'class': 'category'}), required=False)

    def __init__(self, *args, **kwargs):
        # import ipdb; ipdb.set_trace()

        self.categories = kwargs.pop('categories')
        self.base_fields['categories'].choices=self.categories
        super(EventSearchForm, self).__init__(*args, **kwargs)

