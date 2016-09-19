# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views as url_views

urlpatterns = [
    url(r'^$', url_views.home, name='home'),
]