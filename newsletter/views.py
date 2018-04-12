from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core import signing
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from mailchimp3 import MailChimp
from mailchimp3.mailchimpclient import MailChimpError

from .models import Category, Subscriber, Subscription
from .forms import SignupForm

import logging
logger = logging.getLogger(__name__)


def signup(request):
    category = Category.objects.get(tag='general-newsletter')
    form = SignupForm(request.POST or None, category=category, request=request)
    # Manage templates depending on site
    site_id = get_current_site(request).pk
    if site_id == 2:
        template_name = 'comingsoon_signup.html'
    else:
        template_name = 'signup.html'

    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']

            # Mailchimp integration
            api_key = settings.MAILCHIMP_API_KEY
            mc_client = MailChimp(mc_api=api_key)
            # Add subscriber to list
            try:
                mc_client.lists.members.create(category.mailchimp_list_id, {
                    'email_address': email,
                    'status': 'pending',
                })
                return redirect('newsletter:thank-you')
            except MailChimpError:
                messages.error(request, _("This email address is already subscribed"))
    return render(request, template_name, {
        'form': form,
    })


def activation_sent(request):
    site_id = get_current_site(request).pk
    if site_id == 2:
        template_name = 'comingsoon_thankyou.html'
    else:
        template_name = 'thankyou.html'

    return render(request, template_name, {})


def activate_subscription(request, signing_value):
    """
    - Decode the signing_value
    - look up email and tag
    - Save subscription
    - values should be {'tag': tag, 'email': email}
    """
    values = signing.loads(signing_value)
    email = values['email']
    tag = values['tag']
    category = Category.objects.get(tag=tag)

    if Subscriber.objects.filter(email=email, subscriptions=category).exists():
        messages.error(request, _("This subscription is already activated"))
    else:
        subscriber, created = Subscriber.objects.get_or_create(email=email)
        subscriber.subscriptions.add(category)
        messages.success(request, _("Your subscription is activated. Thank you!"))

    return redirect('/')

@csrf_exempt
def mailchimp_webhook(request):
    data = request.POST
    email = data.get('data[email]')
    list_id = data.get('data[list_id]')
    status = data.get('type')
    action = data.get('data[action]')

    if list_id:
        category = Category.objects.get(mailchimp_list_id=list_id)
        if action == 'delete':
            # Completely remove subscription
            subscription = Subscription.objects.filter(subscriber__email=email, category=category).first()
            if subscription:
                subscription.delete()
                logger.info("Subscription for {} removed.".format(email))
        else:
            subscriber, created = Subscriber.objects.get_or_create(email=email)

            # Update subscription
            if status == 'subscribe':
                subscription, created = Subscription.objects.get_or_create(subscriber=subscriber, category=category, defaults={'status': 'subscribe'})
                subscription.status = 'subscribe'
                subscription.save()
            elif status == 'unsubscribe':
                subscription, created = Subscription.objects.get_or_create(subscriber=subscriber, category=category, defaults={'status': 'unsubscribe'})
                subscription.status = 'unsubscribe'
                subscription.save()
            else:
                pass

            logger.info(subscription)

    return HttpResponse(status=200)
