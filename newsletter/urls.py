from django.conf.urls import url

from . import views

app_name = 'newsletter'
urlpatterns = [
    url(r'^$', views.signup, name='signup'),
    url(r'^thank-you/$', views.activation_sent, name='thank-you'),
    url(r'^activate/(?P<signing_value>[\:\w\.\-]+)/$', views.activate_subscription, name='activate'),
]
