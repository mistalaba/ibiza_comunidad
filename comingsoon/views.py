from django.shortcuts import render
from django.views.defaults import page_not_found, server_error

from newsletter.forms import SignupForm

# Create your views here.
def index(request):
    form = SignupForm()
    return render(request, 'index.html', {
        'form': form,
    })

def handler404(request, exception):
    return page_not_found(request, exception, template_name="comingsoon_404.html")

def handler500(request):
    return server_error(request, template_name="comingsoon_500.html")
