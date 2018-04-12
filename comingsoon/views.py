from django.conf import settings
from django.contrib import messages
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.shortcuts import render, redirect
from django.views.defaults import page_not_found, server_error
from django.utils.translation import ugettext_lazy as _

from mailchimp3 import MailChimp
from meta.views import Meta

from newsletter.forms import SignupForm
from newsletter.models import Category

# Create your views here.
def index(request):
    category = Category.objects.get(tag='coming-soon')
    form = SignupForm(request.POST or None, category=category, request=request)

    meta = Meta(
        title=_("Comunidad Ibiza - Local knowledge working together"),
        description=_("The community for crowdsourcing information in Ibiza"),
        image=static('comingsoon/img/comingsoon.jpg'),
        twitter_card='summary_large_image',
        twitter_site='@com_ibiza',
        twitter_creator='@com_ibiza',
        url='/',
        locale='en_us',
    )

    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']

            # Mailchimp integration
            api_key = settings.MAILCHIMP_API_KEY
            mc_client = MailChimp(mc_api=api_key)
            # Add subscriber to list
            mc_client.lists.members.create(category.mailchimp_list_id, {
                'email_address': email,
                'status': 'pending',
            })
            messages.success(request, _("Thank you for subscribing! We have sent a confirmation to your email address, please verify it to continue."))
            return redirect('comingsoon:index')

    return render(request, 'index.html', {
        'form': form,
        'meta': meta,
    })

def handler404(request, exception):
    return page_not_found(request, exception, template_name="comingsoon_404.html")

def handler500(request):
    return server_error(request, template_name="comingsoon_500.html")
