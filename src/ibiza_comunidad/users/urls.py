from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.list_users, name='list-users'),
    url(r'^profile/$', views.private_user_profile, name='private-profile'),
    url(r'^profile/(?P<username>[\w.@+-_]+)/$', views.public_user_profile, name='public-profile'),

    url(regex=r'^~redirect/$', view=views.UserRedirectView.as_view(), name='redirect'),
    # url(regex=r'^(?P<username>[\w.@+-]+)/$', view=views.UserDetailView.as_view(), name='detail'),
    url(regex=r'^~update/$', view=views.UserUpdateView.as_view(),name='update'),

]
