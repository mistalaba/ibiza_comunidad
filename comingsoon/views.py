from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.defaults import page_not_found, server_error
from django.utils.translation import ugettext_lazy as _

from newsletter.forms import SignupForm
from newsletter.models import Category

# Create your views here.
def index(request):
    category = Category.objects.get(tag='coming-soon')
    form = SignupForm(request.POST or None, category=category, request=request)

    if request.method == 'POST':
        if form.is_valid():
            subscriber = form.save()
            return redirect('newsletter:thank-you')

    return render(request, 'index.html', {
        'form': form,
    })

def handler404(request, exception):
    return page_not_found(request, exception, template_name="comingsoon_404.html")

def handler500(request):
    return server_error(request, template_name="comingsoon_500.html")
