from django import forms
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from .models import Subscriber

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
        text_content = 'Welcome to the newsletter.\n\nKind regards,\n/Comunidad Ibiza\n\nUnsubscribe here: %tag_unsubscribe_url%'
        html_content = '<p>Welcome to the newsletter.</p><p>Kind regards,<br>/Comunidad Ibiza</p><p><a href="%tag_unsubscribe_url%">Unsubscribe</a></p>'
        msg = EmailMultiAlternatives(
            'You signed up for {}'.format(self.category),
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [data['email']],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.tags = [self.category.tag]
        msg.send()
