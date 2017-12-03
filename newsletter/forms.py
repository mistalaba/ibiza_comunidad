from django import forms

from .models import Subscriber

class SignupForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
