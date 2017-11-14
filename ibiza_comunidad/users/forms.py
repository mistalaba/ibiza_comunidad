#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms

class ProfileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ProfileForm, self).__init__(*args, **kwargs)

    username = forms.CharField()
    email = forms.EmailField()
