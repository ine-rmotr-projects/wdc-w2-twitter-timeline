from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^login', auth_views.login, {'template_name': 'login.html'}),
    url(r'^logout', views.logout),
    url(r'^tweet/(?P<tweet_id>\d+)/delete', views.delete_tweet),
]
