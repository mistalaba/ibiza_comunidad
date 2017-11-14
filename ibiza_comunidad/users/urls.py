from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^profile/$', views.private_user_profile, name='private-profile'),

    url(regex=r'^$', view=views.UserListView.as_view(), name='list'),
    url(regex=r'^~redirect/$', view=views.UserRedirectView.as_view(), name='redirect'),
    # url(regex=r'^(?P<username>[\w.@+-]+)/$', view=views.UserDetailView.as_view(), name='detail'),
    url(regex=r'^~update/$', view=views.UserUpdateView.as_view(),name='update'),

]
