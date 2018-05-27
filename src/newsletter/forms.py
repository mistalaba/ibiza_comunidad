from django import forms
from django.conf import settings
from django.core import signing
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


from core.utils import remove_unsubscribe
from core.tasks import async_remove_unsubscribe

from .models import Subscriber
from .utils import send_newsletter_signup

class SignupForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.category = kwargs.pop('category')
        self.request = kwargs.pop('request')
        super(SignupForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(max_length=254, required=True, widget=forms.widgets.EmailInput(attrs={'placeholder': _("Enter your email here")}))

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        # Check if the email exist with the category
        if Subscriber.objects.filter(email=cleaned_data['email'], subscriptions=self.category).exists():
            raise forms.ValidationError(_("You are already subscribed"))
        return cleaned_data
