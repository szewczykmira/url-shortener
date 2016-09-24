# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views as url_views

urlpatterns = [
    url(r'^$', url_views.home, name='home'),
    url(r'^!(?P<short_url>.+)/$', url_views.display_info, name='display_info'),
    url(r'^(?P<short_url>.+)/$', url_views.follow_link, name='follow_link'),
]