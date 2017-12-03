from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _

from .forms import SignupForm

def signup(request):
    form = SignupForm(request.POST or None)
    # Manage templates depending on site
    site_id = get_current_site(request).pk
    if site_id == 2:
        template_name = 'comingsoon_signup.html'
    else:
        raise NotImplementedError

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, _("Signup successful"))
            return redirect('newsletter:thank-you')

    return render(request, template_name, {
        'form': form,
    })

def thankyou(request):
    site_id = get_current_site(request).pk
    if site_id == 2:
        template_name = 'comingsoon_thankyou.html'
    else:
        raise NotImplementedError

    return render(request, template_name, {})
