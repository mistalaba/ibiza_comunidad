from django.shortcuts import render
from django.views.defaults import page_not_found, server_error

# Create your views here.
def index(request):
    return render(request, 'index.html', {
        })

def handler404(request, exception):
    return page_not_found(request, exception, template_name="comingsoon_404.html")
