# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from forms import ShortURLForm


def home(request):
    ctx = {'form': ShortURLForm(request.POST or None)}
    if request.method == 'POST':
        print request.POST
        origin_url = request.POST.get('origin_url', False)
    return render(request, "url_shortener/home.html", ctx)
