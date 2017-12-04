from django import forms
from django.conf import settings
from django.core.mail import EmailMessage

from .models import Subscriber

# class SignupForm(forms.ModelForm):
#     class Meta:
#         model = Subscriber
#         fields = ['email']

class SignupForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.category = kwargs.pop('category')
        super(SignupForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(max_length=254, required=True)

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        # Check if the email exist with the category
        if Subscriber.objects.filter(email=cleaned_data['email'], subscriptions=self.category).exists():
            raise forms.ValidationError("You are already subscribed to this")
        return cleaned_data

    def save(self):
        data = self.cleaned_data
        subscriber, created = Subscriber.objects.get_or_create(email=data['email'])
        subscriber.subscriptions.add(self.category)
        # Send confirmation
        msg = EmailMessage(
            'You signed up for {}'.format(self.category),
            'Welcome to the newsletter.\n\nKind regards,\n/Comunidad Ibiza',
            settings.DEFAULT_FROM_EMAIL,
            [data['email']],
        )
        msg.tags = [self.category.tag]
        msg.send()
