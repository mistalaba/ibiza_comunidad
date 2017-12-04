from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _

from .models import Category
from .forms import SignupForm

def signup(request):
    category = Category.objects.get(tag='coming-soon')
    form = SignupForm(request.POST or None, category=category)
    # Manage templates depending on site
    site_id = get_current_site(request).pk
    if site_id == 2:
        template_name = 'comingsoon_signup.html'
    else:
        template_name = 'signup.html'

    if request.method == 'POST':
        if form.is_valid():
            subscriber = form.save()
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
        template_name = 'thankyou.html'

    return render(request, template_name, {})
