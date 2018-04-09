from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^login', auth_views.login, {'template_name': 'login.html'}),
    url(r'^logout', views.logout),
    url(r'^follow', views.follow),
    url(r'^unfollow', views.unfollow),
    url(r'^tweet/(?P<tweet_id>\d+)/delete', views.delete_tweet),
    url(r'^tweet/(?P<tweet_id>\d+)/like', views.like_tweet),
    url(r'^(?P<username>\w+)$', views.home),
    url(r'^$', views.home),
]
