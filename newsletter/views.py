from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core import signing
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _

from .models import Category, Subscriber
from .forms import SignupForm

import logging
logger = logging.getLogger(__name__)


def signup(request):
    category = Category.objects.get(tag='coming-soon')
    form = SignupForm(request.POST or None, category=category, request=request)
    # Manage templates depending on site
    site_id = get_current_site(request).pk
    if site_id == 2:
        template_name = 'comingsoon_signup.html'
    else:
        template_name = 'signup.html'

    if request.method == 'POST':
        if form.is_valid():
            subscriber = form.save()
            return redirect('newsletter:thank-you')

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
