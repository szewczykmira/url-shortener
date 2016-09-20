# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from forms import ShortURLForm


def home(request):
    ctx = {'form': ShortURLForm(request.POST or None)}
    if request.method == 'POST':
        user = False
        if not user:
            ctx['form'].add_error(None, _("There is no user in databsase"))
        if ctx['form'].is_valid():
            # TODO: if url in db then redirect to it's information
            url = ctx['form'].save(commit=False)
            url.user = user
            url.set_short_url()
            url.save()
            # TODO: add message, redirect
    return render(request, "url_shortener/home.html", ctx)
