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

    def save(self):
        """
        New logic:
        - Create a signing thingy here, using the tag and subscriber email address.
        - Add it to the email
        - When subscriber clicks the link, go to activate_subscription, where we save the email and the tag.
        """
        data = self.cleaned_data

        # Check if the email is on the unsubscribe list
        async_remove_unsubscribe.delay(data['email'], self.category.tag)


        signing_value = signing.dumps({"tag": self.category.tag, 'email': data['email']})

        # Send confirmation
        signing_url = reverse('newsletter:activate', kwargs={'signing_value': signing_value})
        url = self.request.build_absolute_uri(signing_url)

        c = {
            'subject': _("Confirm your subscription"),
            'recipient_email': data['email'],
            'category': self.category,
            'button_link': url,
            'button_text': _("Confirm email")

        }
        send_newsletter_signup(self.request, c)

        # text_content = 'Welcome to the newsletter.\nPlease activate your subscription by this link: {}\n\nKind regards,\n/Comunidad Ibiza\n\nUnsubscribe here: %tag_unsubscribe_url%'.format(url)
        # html_content = '<p>Welcome to the newsletter.<br>Please activate your subscription <a href="{}">here</a></p><p>Kind regards,<br>/Comunidad Ibiza</p><p><a href="%tag_unsubscribe_url%">Unsubscribe</a></p>'.format(url)
        # msg = EmailMultiAlternatives(
        #     'You signed up for {}'.format(self.category),
        #     text_content,
        #     settings.DEFAULT_FROM_EMAIL,
        #     [data['email']],
        # )
        # msg.attach_alternative(html_content, "text/html")
        # msg.tags = [self.category.tag]
        # msg.send()
