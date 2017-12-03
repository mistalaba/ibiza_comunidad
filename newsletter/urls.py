from django.conf.urls import url

from . import views

app_name = 'newsletter'
urlpatterns = [
    url(r'^$', views.signup, name='signup'),
    url(r'^thank-you/$', views.signup, name='thank-you'),
]
